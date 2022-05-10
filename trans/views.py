from django.shortcuts import render
from googletrans import Translator
import googletrans

# Create your views here.

def index(req):
    context={               # get전송일 때 넘겨주는 context
        # "d" : {1:"one", 2:"two", 3:"three"}   # 딕셔너리 자료형 연습
        "na" : googletrans.LANGUAGES    # 얘를 위해서 import googletrans 해 준 거임 
    }  
    if req.method=='POST':
        t=req.POST.get("con")
        fn=req.POST.get("fn")
        tn=req.POST.get("tn")
        translator=Translator()
        trans=translator.translate(t, src=fn, dest=tn)
        # print(trans.text) # 이 친구가 화면의 오른쪽으로 나와야 하기 때문에 context로 넘겨줘야 한다!!
        context.update({    # 딕셔너리에는 update라는 매서드가 있어서 다시 적어주는 것 보다 update해 주는게 낫다 > get이던 post던 na는 넘겨준다
            "trans" : trans.text,
            "con" : t,            # 해주고 index에서 찍어야 한다 {{ trans }}  
            "fn" : fn,              # 화면에 떠 있게 할려면 여기서 무조건 넘겨 주어야 한다 !!! 
            "tn" : tn,                  # 그래야 index에서 조건 설정 해 주었을 때 selected 되 있음 ! (여기서 안 넘겨주면 조건 걸어줘도 안 떠있다)
        })                                    
    return render(req, "trans/index.html", context) # 근데 여기서 get 전송일 때 context를 만난적이 없으니 에러가 난다 !!! (unboundlocal error)
                                                    # 그래서 맨 위에 get 전송일 때도 context를 넘겨줘야 한다 !!
