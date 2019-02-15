from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def register(request):
    if request.method == 'POST':
        messages=[]
        username = request.POST['name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if username=='':
            messages.append('用户名不能为空')
            return render(request, 'login/register.html', locals())
        if password1=='':
            messages.append('密码不能为空')
            return render(request, 'login/register.html', locals())
        if password1 != password2:
            messages.append('两次输入密码不同！')
            return render(request, 'login/register.html', locals())
        same_name_user = User.objects.filter(username=username)
        if same_name_user:
            messages.append('用户名已存在，请重新输入')
            return render(request, 'login/register.html', locals())
        same_email_user = User.objects.filter(email=email)
        if same_email_user:
            messages.append('邮箱已被注册，请重新输入邮箱')
            return render(request, 'login/register.html', locals())
        new_user = User.objects.create()
        new_user.username = username
        new_user.password = make_password(password1)
        new_user.email = email
        new_user.is_staff =1
        new_user.save()
        return render(request,'login/redirect.html')
    else:
        return render(request,'login/register.html',locals())

def logout(request):
    pass
    return  redirect('cloud:index')
