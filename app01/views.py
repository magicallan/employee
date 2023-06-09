from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from django import forms
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe


# Create your views here.
def register(request):
    return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')


def depart_list(request):
    """部门列表"""
    queryset = models.Department.objects.all()

    return render(request, 'depart_list.html', {"queryset": queryset})


def depart_add(request):
    """添加部门"""
    if request.method == "GET":
        return render(request, 'depart_add.html')
    title = request.POST.get("title")
    models.Department.objects.create(title=title)
    return redirect("/depart/list/")


def depart_delete(request):
    """删除部门"""
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")


def depart_use(request, nid):
    # """编辑部门"""
    if request.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_use.html', {"row_object": row_object})
    # title = request.POST.get("title")
    # models.Department.objects.filter(id=nid).update(title=title)
    # return redirect("/depart/list/")


# 加载文件上传表单
def upload(request):
    return render(request, "upload.html")


# 执行文件上传处理
def img_upload(request):
    my_file = request.FILES.get("pic", None)
    if not my_file:
        return HttpResponse("没有上传的文件信息")
    destination = open("./app01/static/img/a.jpg", "wb+")
    for chunk in my_file.chunks():
        destination.write(chunk)
    destination.close()

    return HttpResponse("上传的文件:")

def pt_upload(request):
    my_file = request.FILES.get("pic", None)
    if not my_file:
        return HttpResponse("没有上传的文件信息")
    destination = open("./app01/static/model/a.pt", "wb+")
    for chunk in my_file.chunks():
        destination.write(chunk)
    destination.close()

    return HttpResponse("上传的文件:")


def user_list(request):
    queryset = models.UserInfo.objects.all()
    return render(request, 'user_list.html', {"queryset": queryset})


class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "age", "gender", "account", "creat_time", "depart"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # if name == "password":
            #     field.widget.
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}


def user_add(request):
    if request.method == "GET":
        form = UserModelForm()
        return render(request, 'user_add.html', {"form": form})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/user/list/")

    return render(request, 'user_add.html', {"form": form})


def user_edit(request, nid):
    """编辑用户"""
    row_object = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        # 根据ID区数据库获取要编辑的那一行数据
        form = UserModelForm(instance=row_object)
        return render(request, 'usr_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_add.html', {"form": form})


def user_delete(request, nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect("/user/list/")


def pnum_list(request):
    data_dict = {}
    search_data = request.GET.get('q', "")
    if search_data:
        data_dict["mobile__contains"] = search_data

    page = int(request.GET.get('page', 1))
    page_size = 10  # 每页显示数据
    start = (page - 1) * page_size
    end = page * page_size
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")[start:end]
    # 数据总条数
    total_count = models.PrettyNum.objects.filter(**data_dict).order_by("-level").count()
    # 总页码
    total_page_count, div = divmod(total_count, page_size)
    if div:
        total_page_count += 1

    page_str_list = []
    for i in range(1, total_page_count + 1):
        ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)
    page_string = mark_safe("".join(page_str_list))
    return render(request, 'pnum_list.html',
                  {"queryset": queryset, "search_data": search_data, "page_string": page_string}
                  )


class PrettyModelForm(forms.ModelForm):
    class Meta:
        model = models.PrettyNum
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    # 验证：方式2
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise forms.ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            raise forms.ValidationError("格式错误")
        return txt_mobile


def pnum_add(request):
    if request.method == "GET":
        form = PrettyModelForm()
        return render(request, 'pnum_add.html', {"form": form})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect("/pnum/list/")

    return render(request, 'pnum_add.html', {"form": form})


class PrettyEditModelForm(forms.ModelForm):
    # mobile = forms.CharField(disabled=True, label="手机号")
    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise forms.ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            raise forms.ValidationError("格式错误")
        return txt_mobile


def pnum_edit(request, nid):
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == "GET":
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'pnum_edit.html', {"form": form})

    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pnum/list/')

    return render(request, 'pnum_edit.html', {"form": form})


def pnum_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/pnum/list/")
