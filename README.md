# 对抗攻击
让你的模型更加安全
## 项目介绍
本项目是使用Django框架开发的Web应用程序，该程序实现了用户登录及验证，模型上传与测试功能
## 使用
### 安装
克隆该项目 git clone https://github.com/magicallan/employee.git
### 配置数据库
需要在本地使用Mysql创建一个名为web的数据库
并在employee/settings.py文件中修改PASSWORD字段为你自己数据库的密码
<img width="334" alt="image" src="https://github.com/magicallan/employee/assets/116506161/3dd2d1b6-feb4-4501-887b-447ea565d11d">
### 进行数据库迁移
在终端中顺序执行以下语句：

python manage.py makemigrations

python manage.py migrate

运行成功后显示如下

<img width="223" alt="image" src="https://github.com/magicallan/employee/assets/116506161/e8687280-1a7a-46bf-a022-37f700147a49">

### web端使用
运行django服务器
显示如下
<img width="726" alt="image" src="https://github.com/magicallan/employee/assets/116506161/bfa56384-ecf4-4d0b-a0b9-41a75233a309">

点击此链接即显示web端
<img width="1080" alt="image" src="https://github.com/magicallan/employee/assets/116506161/0a08959f-7ff5-4596-85ac-27c81bdfb8ba">
可进行注册，注册后自动跳转登录界面
登录后及展示模型列表
<img width="1078" alt="image" src="https://github.com/magicallan/employee/assets/116506161/e68a0fa9-b6f5-48ac-af1c-f86a598d41a5">

该页面点击上传模型即可添加要攻击的模型

<img width="883" alt="image" src="https://github.com/magicallan/employee/assets/116506161/29b7af0d-dfaa-41f6-85f4-3ddff1dbaa42">

注意：上传的模型必须是*.pt文件

点击测试按钮即可对模型进行攻击测试，点击删除按钮可删除已有模型

上传照片并取名，几秒钟后便会展示本机过后的图片及模型被攻击过后预测的类别

<img width="656" alt="image" src="https://github.com/magicallan/employee/assets/116506161/84971dad-7fb7-424c-a268-38d4634159f9">
