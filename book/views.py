from django.shortcuts import redirect, render
from .models import Book

# Create your views here.

def create(req):
    if req.method == "POST":
        im=req.POST.get("impo")
        sn=req.POST.get("sname")
        su=req.POST.get("surl")
        sc=req.POST.get("scon")
        # print(im,sn,su,sc)
        Book(site_name=sn, site_url=su, site_con=sc, impo=bool(im), maker=req.user).save()  # on을 bool로 바꾸면 True 나옴
        return redirect("book:index")                                                       # impo 체크 되어 있으면 :on 이라고 되있음
    return render(req, "book/create.html")

def index(req):
    b=req.user.book_set.all()   # 사용자들 마다 자신들이 즐겨찾기 한 북들 다 나와
    context={
        "bset" : b,
    }
    return render(req, "book/index.html", context)