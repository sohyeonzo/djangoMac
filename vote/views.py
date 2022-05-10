from django.shortcuts import redirect, render
from .models import Topic, Choice
from django.utils import timezone
# Create your views here.

def delete(req, tpk):
    t=Topic.objects.get(id=tpk)
    if t.maker == req.user:
        t.delete()
    else:
        pass    #혼내줌(경고 메세지)
    return redirect("vote:index")

def create(req):
    if req.method=="POST":
        s=req.POST.get("sub")
        c=req.POST.get("con")
        cn=req.POST.getlist("cname")
        cp=req.FILES.getlist("cpic")
        cc=req.POST.getlist("ccom")
        # print(s,c,cn,cp,cc)
        # print(req.POST)
        t=Topic(subject=s, maker=req.user, content=c, pubdate=timezone.now())
        t.save()
        for name, pic, con in zip(cn, cp, cc): #얘네도 리스트임
            Choice(topic=t, name=name, pic=pic, con=con).save()
        return redirect("vote:index")
    return render(req, "vote/create.html")

def cancel(req, tpk):
    t=Topic.objects.get(id=tpk)
    t.voter.remove(req.user)
    req.user.choice_set.get(topic=t).choicer.remove(req.user)   #user 입장에서 골랐던 애들 다 나와 그 중 get > 해당 보기를 가져온다 > 그 xhoicer 를 지운다
    return redirect("vote:detail", tpk)

def vote(req, tpk):
    t=Topic.objects.get(id=tpk)
    if not req.user in t.voter.all():   # 다중 투표 막기 위해 (아거 하고 서버 돌리고 admin, vote 페이지 따로 킨 다음 투표 확인해 보면 다중 투표 안 되고, 투표는 잘 됨)
        t.voter.add(req.user)
        cpk=req.POST.get("cho")
        c=Choice.objects.get(id=cpk)
        c.choicer.add(req.user)
    return redirect("vote:detail", tpk)

def detail(req, tpk):
    t=Topic.objects.get(id=tpk)
    c=t.choice_set.all()
    context={
        "t" : t,
        "cset" : c,
    }
    return render(req, "vote/detail.html", context)

def index(req):
    t=Topic.objects.all()
    context={
        "tset" : t,
    }
    return render(req, 'vote/index.html', context)
