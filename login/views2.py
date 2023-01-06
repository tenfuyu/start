from django.shortcuts import render,redirect
from index import forms
from . import models
# Create your views here.


def login(request):
    if request.method == 'POST':
        form = forms.UserForm(data=request.POST)
        if form.is_valid():
            n = form.cleaned_data.get('fake_name')
            p = form.cleaned_data.get('password')
            if models.User.objects.filter(fake_name=n).first():
                o = models.User.objects.filter(fake_name=n).first()
                if o.password == p:
                    request.session['info'] = {'id':o.id,'fake_name':o.fake_name}
                    if o.fake_name == 'admin':
                        return redirect('/admin/')
                    return redirect('/')
                return render(request, 'login.html', {'form': form, 'error': "密码错误"})
            return render(request, 'login.html', {'form': form, 'error': "用户不存在"})
    form = forms.UserForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method=='POST':
        form = forms.RegisterForm(data=request.POST)
        if form.is_valid():
            if request.POST.get('password2') == form.cleaned_data.get('password'):
                form.save()
                return redirect('/login/')
            form = forms.RegisterForm()
            return render(request, 'register.html', {'form': form,'error':'两次输入的密码不一致'})
        form = forms.RegisterForm()
        return render(request, 'register.html', {'form': form, 'error': '该用户已存在'})
    form = forms.RegisterForm()
    return render(request, 'register.html',{'form':form})


def info(request, name):
    from django.db.models import Count
    from django.utils.safestring import mark_safe
    inf = request.session.get('info')
    if not inf:
        return redirect('/login/')
    u2 = models.User.objects.filter(id=inf['id']).first()
    u = models.User.objects.filter(fake_name=name).first()
    bl = models.Box.objects.filter(sender=name).all()
    fold_title = models.Fold.objects.filter(creator=name,box_id=666).all()
    h = models.PickHistory.objects.filter(picker=u2).all()
    p = int(request.GET.get('page', 1))
    page_size = 10
    st = (p - 1) * page_size
    en = p * page_size
    page_list = []
    num = h.aggregate(num=Count('id'))['num']
    if num % page_size == 0:
        pages = num //page_size
    else:
        pages = num // page_size + 1
    for i in range(1, pages + 1):
        ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_list.append(ele)
    page_str = mark_safe(''.join(page_list))
    obj = h[st:en]
    return render(request, 'info.html', {'n': name,'user':u,'bl':bl,'u2':u2,'h':obj,'str':page_str,'ft':fold_title})


def login_out(request):
    request.session.clear()
    return redirect('/')
