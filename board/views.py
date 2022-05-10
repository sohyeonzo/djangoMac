from django.shortcuts import render, redirect
from board.models import Board, Reply
from django.utils import timezone   # ✨
from django.core.paginator import Paginator
# Create your views here.
from django.contrib import messages


def unlikey(req, bpk):
    b=Board.objects.get(id=bpk)
    b.likey.remove(req.user)
    return redirect("board:detail", bpk)

def likey(req, bpk):
    b=Board.objects.get(id=bpk)
    b.likey.add(req.user)
    return redirect("board:detail", bpk)

def index(req):
    pg=req.GET.get("page",1)
    cate=req.GET.get("cate", "")    # cate가 넘어오지 않으면 빈 문자열로 처리
    kw=req.GET.get("kw", "")

    if kw:
        if cate == "sub":
            b=Board.objects.filter(subject__startswith=kw)
        elif cate == "wri":
            try:
                from acc.models import User # 레코드로 분류 해야해서
                u=User.objects.get(username=kw) # 레코드 자체를 가져와야한다
                b=Board.objects.filter(writer=u) 
            except:
                b=Board.objects.none()
        elif cate == "con":
            b=Board.objects.filter(content__contains=kw)
        else:
            b=Board.objects.all() 
    else:
        b=Board.objects.all() 
    
    b=b.order_by("-pubdate")    # - 붙으면 내림차순 > 최신글이 위로

    pag=Paginator(b, 5) # b 레코드를 5개씩 보따리
    obj=pag.get_page(pg)
    context={
        "bset" : obj,
        "kw" : kw,
        "cate" : cate,
    }
    return render(req, "board/index.html", context)

def dreply(req, bpk, rpk):
    r=Reply.objects.get(id=rpk)
    if req.user==r.replyer:
        r.delete()
    else:
        messages.error(req, "사용자가 일치하지 않습니다")    # 경고메세지 예쩡
    return redirect("board:detail", bpk)

def creply(req, bpk):
    b=Board.objects.get(id=bpk)
    c=req.POST.get("com")
    Reply(board=b, replyer=req.user, comment=c).save() 
    return redirect("board:detail", bpk)

def create(req):
    if req.method=="POST":
        s=req.POST.get("sub")
        c=req.POST.get("con")
        Board(subject=s, writer=req.user, content=c, pubdate=timezone.now()).save() # ✨
        return redirect("board:index")
    return render(req, "board/create.html")

def delete(req, bpk):
    b=Board.objects.get(id=bpk)
    if b.writer == req.user:    # 같을때만 삭제 하도록
        b.delete()
    else:   #hacking
        messages.error(req, "계정 정보가 일치하지 않습니다")    #경고 메세지
    return redirect("board:index")

def update(req, bpk):
    b=Board.objects.get(id=bpk)
    if b.writer != req.user:
        messages.error(req, "혼난다!") # 경고메시지 대기중
        return redirect("board:index")
    if req.method=="POST":
        s=req.POST.get("sub")
        c=req.POST.get("con")
        b.subject=s
        b.content=c 
        b.save() 
        return redirect("board:detail", bpk)
    context={
        "b" : b
    }
    return render(req, "board/update.html", context)

def detail(req, bpk):
    b=Board.objects.get(id=bpk)
    r=b.reply_set.all()
    context={
        "b" : b,
        "rset" : r
    }
    return render(req, "board/detail.html", context)

