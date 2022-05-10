from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password

from .models import User
from django.contrib import messages
# Create your views here.

def delete(req):
    # print(req.POST.get("pwck"))
    pw=req.POST.get("pwck")
    if check_password(pw, req.user.password):  # 비문
        req.user.delete()
        return redirect("acc:index")
    else:
        messages.error(req, "패스워드가 틀렸습니다.")    # 사용자의 요청에 메시지 넣어줌
        return redirect("acc:profile")


def signup(req):
    if req.method=="POST":
        un=req.POST.get("uname")
        up=req.POST.get("upass")
        uc=req.POST.get("ucomm")
        pi=req.FILES.get("upic")
        User.objects.create_user(username=un, password=up, comment=uc, pic=pi)
        return redirect("acc:login")
    return render(req, "acc/signup.html")

def update(req):
    if req.method=="POST":
        u=req.user
        up=req.POST.get("upass")
        uc=req.POST.get('ucomm')
        pi=req.POST.get("upic")
        ue=req.POST.get("umail")
        if up:      #password 가 있으면
            u.set_password(up)
        if pi:
            u.pic=pi
        u.comment=uc
        u.email=ue
        u.save()
        login(req, u)   # 다시 로그인 되게 하는 것 (이 부분 빼면 다시 로그인 페이지로 가는 거)
        return redirect("acc:profile")
    return render(req, "acc/update.html")

def profile(req):
    return render(req, "acc/profile.html")

def logout_user(req):
    logout(req)
    return redirect("acc:index")

def login_user(req):
    if req.method=="POST":
        un=req.POST.get("uname")
        up=req.POST.get("upass")
        u=authenticate(username=un, password=up)
        # print(u)
        if u:
            login(req, u)
            messages.success(req, f"{u} WELCOME :D !")
            return redirect("acc:index")
        else:
            messages.error(req, "계정정보가 일치하지않습니다.")    # 메시지 넣어줄 곳!
    return render(req, "acc/login.html")

def index(req):
    return render(req, "acc/index.html")
