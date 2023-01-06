from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls.base import reverse
import index.forms
from login import models
from index import forms
from django.core.mail import send_mail
from django.utils.safestring import mark_safe

# Create your views here.
# 调用sender,html内使用sender_id


def fold3(request,name,box):
    u = models.User.objects.filter(fake_name=name).first()
    b = models.Box.objects.filter(id=box).first()
    if request.method == 'POST':
        f=models.Fold.objects.filter(fold_id=request.POST.get('fold')).first()
        models.Fold.objects.create(box_id=b,creator=u,fold_id=f.fold_id,fold_name=f.fold_name)
        return redirect(reverse('box',kwargs={'id':box}))
    fol = models.Fold.objects.filter(creator=u, box_id=666).all()
    if fol:
        return render(request,'f3.html',{'fol':fol})
    return redirect(reverse('fold2',kwargs={'id':name}))


def fold2(request, id):
    ft =models.Fold.objects.filter(fold_id=id,box_id=666).first()
    fc = models.Fold.objects.filter(fold_id=id).all().exclude(box_id=666)
    li=[]
    for i in fc:
        b=models.Box.objects.filter(id=i.box_id.id).first()
        li.append(b)
    return render(request,'fc.html',{'fc':li,'ft':ft})


def fold(request):
    if request.method == 'POST':
        u=models.User.objects.filter(id=request.session.get('info')['id']).first()
        b=models.Box.objects.filter(id=666).first()
        name = request.POST.get('name')
        import os
        from pathlib import Path
        BASE_DIR = Path(__file__).resolve().parent.parent
        ad = os.path.join(BASE_DIR, r'static\media\img\\')
        f = request.FILES.get('surface')
        f2 = open(ad + f.name, mode='wb')
        for chunk in f.chunks():
            f2.write(chunk)
        f2.close()
        num=models.Fold.objects.filter(box_id=b).count()
        models.Fold.objects.create(box_id=b,creator=u,fold_name=name,fold_id=num+1,img=r'img\\'+f.name)
        return redirect(reverse('info',kwargs={'name':u.fake_name}))
    return render(request,'fold.html')


def change_head(request):
    if request.method == 'POST':
        import os
        from pathlib import Path
        BASE_DIR = Path(__file__).resolve().parent.parent
        ad=os.path.join(BASE_DIR, r'static\media\img\\')
        f = request.FILES.get('head')
        f2 = open(ad+f.name,mode='wb')
        for chunk in f.chunks():
            f2.write(chunk)
        f2.close()
        inf=request.session.get('info')
        o=models.User.objects.filter(id=inf['id']).first()
        o.photo=r'img\\'+f.name
        o.save()
        return redirect(reverse('info',kwargs={'name':o.fake_name}))
    return render(request,'change_head.html')



def search_school(request):
    key=request.GET.get('key',0)
    if key == 0:
        return render(request,'search_school.html')
    obj=models.Box.objects.filter(school=key).all()
    if obj:
        return render(request,'search_school.html',{'obj':obj})
    return render(request,'search_school.html',{'error':'没有搜索到结果哦~'})

def send_sms_code(to_email):
    import random
    sms_code = '%06d' % random.randint(0, 999999)
    EMAIL_FROM = "2427075113@qq.com"
    email_title = '邮箱激活'
    email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(sms_code)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [to_email])
    if send_status==1:
        return sms_code
    return 0
def email(request):
    if request.method == 'POST':
        form=forms.FindForm(data=request.POST)
        if form.is_valid():
            e=form.cleaned_data.get('email')
            if models.User.objects.filter(email=e).first():
                to_email=e
                feedback=send_sms_code(to_email)
                if feedback:
                    form2=forms.RePassword()
                    request.session['temp']={'code':feedback,'user':e}
                    return redirect(reverse(find_code))
                return render(request,'find.html',{'form':form,'h':0,'error':'邮箱无效!'})
            return render(request, 'find.html', {'form': form, 'h': 0, 'error': '用户不存在!'})
    form=forms.FindForm()
    return render(request,'find.html',{'form':form,'h':0})
def find_code(request):
    code=request.session.get('temp')['code']
    if request.method == 'POST':
        if request.POST.get('code') == code:
            return redirect(reverse('re_password'))
        return render(request,'find.html',{'h':1,'error2':'验证码错误！'})
    return render(request,'find.html',{'h':1})
def re_password(request):
    e = request.session.get('temp')['user']
    o= models.User.objects.filter(email=e).first()
    if request.method == 'POST':
        form=forms.RePassword(request.POST)
        if form.is_valid():
            password=form.cleaned_data.get('re_password')
            if request.POST.get('password2')== password:
                o.password=password
                o.save()
                request.session.clear()
                return redirect(reverse('login'))
            form = forms.RePassword()
            return render(request,'re_password.html',{'error':'两次输入的密码不一致！','form':form})
    form=forms.RePassword()
    return render(request,'re_password.html',{'form':form})


def hi(request):
    inf = request.session.get('info')
    if not inf:
        return render(request, 'index.html', {'h': 0})
    import random
    random.seed()
    n = models.Box.objects.all()
    n_nan = models.Box.objects.filter(gender=1).all()
    n_nv = models.Box.objects.filter(gender=2).all()
    li = [i.id for i in n]
    m = random.choice(li)
    li_nan = [i.id for i in n_nan]
    nan = random.choice(li_nan)
    li_nv = [i.id for i in n_nv]
    nv = random.choice(li_nv)
    return render(request, 'index.html', {'h': 1, 'user': inf['fake_name'], 'm': m, 'nan':nan, 'nv':nv})


def box_del(request, id):
    inf = request.session.get('info')
    u = models.User.objects.filter(id=inf['id']).first()
    models.Box.objects.filter(id=id).delete()
    return redirect(reverse('info', args=[u.fake_name]))


def ad_box_del(request, id):
    inf = request.session.get('info')
    if inf['fake_name'] != 'admin':
        return redirect('/')
    models.Box.objects.filter(id=id).delete()
    return redirect(reverse('admin'))


def admin(request):
    from django.db.models import Count
    inf = request.session.get('info')
    if inf['fake_name'] != 'admin':
        return redirect('/')
    p = int(request.GET.get('page', 1))
    page_size=10
    st = (p - 1) *page_size
    en = p * page_size
    page_list=[]
    num=models.Box.objects.aggregate(box_num=Count('id'))['box_num']
    if num%page_size==0:
        pages=num//page_size
    else:
        pages=num//page_size+1
    for i in range(1,pages+1):
        ele='<li><a href="?page={}">{}</a></li>'.format(i,i)
        page_list.append(ele)
    page_str=mark_safe(''.join(page_list))
    obj = models.Box.objects.all()[st:en]
    return render(request, 'admin.html', {'obj': obj, 'str':page_str})


def put(request):
    inf = request.session.get('info')
    if not inf:
        return redirect('/login/')
    if request.method == 'POST':
        inf = request.session.get('info')
        u = models.User.objects.filter(id=inf['id']).first()
        form = forms.BoxForm(request.POST)
        if form.is_valid():
            import re
            a = form.cleaned_data.get('phone')
            if a:
                if re.match(r'\d{11}', a):
                    models.Box.objects.create(**form.cleaned_data, sender=u)
                    return redirect('/')
                form = forms.BoxForm()
                return render(request, 'input.html', {'form': form,'error':"电话号码格式错误"})
            models.Box.objects.create(**form.cleaned_data, sender=u)
            return redirect('/')
    form = forms.BoxForm()
    return render(request, 'input.html', {'form': form})


def next_content(request,id):
    inf = request.session.get('info')
    if not inf:
        return redirect('/login/')
    n_nan = models.Box.objects.filter(gender=1).all()
    n_nv = models.Box.objects.filter(gender=2).all()
    li_nan = [i.id for i in n_nan]
    li_nv = [i.id for i in n_nv]
    if id in li_nv:
        h = li_nv.index(id)
        l = li_nv
        num = len(l)-1
        if h < num:
            next_id=l[h+1]
            nexter=models.Box.objects.filter(id=next_id).first()
        else:
            nexter = 0
        if h > 1:
            form_id=l[h-1]
            former=models.Box.objects.filter(id=form_id).first()
        else:
            former = 0
    else:
        h = li_nan.index(id)
        l = li_nan
        num = len(l)-1
        if h < num:
            next_id = l[h + 1]
            nexter = models.Box.objects.filter(id=next_id).first()
        else:
            nexter = 0
        if h > 1:
            form_id = l[h - 1]
            former = models.Box.objects.filter(id=form_id).first()
        else:
            former = 0
    u2 = models.User.objects.filter(id=inf['id']).first()
    box = models.Box.objects.filter(id=id).first()
    if inf['fake_name'] != 'admin':
        models.PickHistory.objects.create(box=box, picker=u2)
    com = models.Comment.objects.filter(to_box=id).all()
    return render(request, 'content.html', {'user': box, 'com': com, 'u': u2,'h':h,'l':l, 'n':nexter,'f':former,'num':num})


def content(request, id):
    inf = request.session.get('info')
    if not inf:
        return redirect('/login/')
    u2 = models.User.objects.filter(id=inf['id']).first()
    box = models.Box.objects.filter(id=id).first()
    com = models.Comment.objects.filter(to_box=id).all()
    inf_com = []
    for i in com:
        infc = models.InfComment.objects.filter(to_comment=i).all()
        for j in infc:
            inf_com.append(j)
    if inf['fake_name'] != 'admin':
        models.PickHistory.objects.create(box=box, picker=u2)
    return render(request, 'content.html', {'user': box, 'com': com,'u': u2,'inf_com':inf_com})


def comment2(request,id,id2):
    box = models.Box.objects.filter(id=id).first()
    com=models.Comment.objects.filter(id=id2).first()
    com_li = models.Comment.objects.filter(to_box=id).all()
    u = request.session.get('info')
    u2 = models.User.objects.filter(id=u['id']).first()
    if request.method == 'POST':
        form2 = index.forms.CommentForm(request.POST)
        if form2.is_valid():
            c = form2.cleaned_data.get('content')
            models.InfComment.objects.create(content=c, sender=u2, to_comment=com)
            return redirect(reverse('box', args=[id]))
    form2 = index.forms.CommentForm()
    return render(request, 'content.html', {'user': box, 'com': com_li, 'form2': form2})


def comment(request, id):
    inf = request.session.get('info')
    if not inf:
        return redirect('/login/')
    box = models.Box.objects.filter(id=id).first()
    com = models.Comment.objects.filter(to_box=id).all()
    u = request.session.get('info')
    u2 = models.User.objects.filter(id=u['id']).first()
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            c = form.cleaned_data.get('content')
            models.Comment.objects.create(content=c, sender=u2, to_box=box)
            return redirect(reverse('box', args=[id]))
    form = index.forms.CommentForm()
    return render(request, 'content.html', {'user': box, 'com': com, 'form': form })


def com_del(request, id, id2):
    inf = request.session.get('info')
    if not inf:
        return redirect('/login/')
    o = models.Comment.objects.filter(id=id2).first()
    if inf['fake_name'] != o.sender_id:
        return HttpResponse('您无权限操作！')
    models.Comment.objects.filter(id=id2).delete()
    return redirect(reverse('box', args=[id]))


def com_del2(request, id, id2):
    inf = request.session.get('info')
    if not inf:
        return redirect('/login/')
    o = models.InfComment.objects.filter(id=id2).first()
    if inf['fake_name'] != o.sender_id:
        return HttpResponse('您无权限操作！')
    models.InfComment.objects.filter(id=id2).delete()
    return redirect(reverse('box', args=[id]))