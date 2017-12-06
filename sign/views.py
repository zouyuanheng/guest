#coding=utf-8

from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from models import Guest,Event
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.

def index(request):
    return render(request,"index.html")
def login_action(request):
    if request.method=='POST':
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
        #if username=='admin' and  password=='admin123':
            response=HttpResponseRedirect('/event_manage/')
            #response.set_cookie('user',username,3600)
            request.session['user']=username
            return response
        else:
            return render(request,"index.html",{'error':'username or password error!'})
    else:
        return render(request,"index.html",{'error':'username or password error!'})
#@login_required
def event_manage(request):
    #username=request.COOKIES.get('user','')
    event_list=Event.objects.all()
    username=request.session.get('user','')
    paginator=Paginator(event_list,2)
    page=request.GET.get('page')
    try:
        contacts=paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer,deliver first page.
        contacts=paginator.page(1)
    except EmptyPage:
        #If page is out of range (e.g. 9999),deliver last page of results.
        contacts=paginator.page(paginator.num_pages)
    return render(request,"event_manage.html",{"user":username,"events":contacts})

#@login_required
def search_name(request):
    username=request.session.get('user','')
    search_name=request.GET.get("name","")
    event_list=Event.objects.filter(name__contains=search_name)
    paginator=Paginator(event_list,2)
    page=request.GET.get('page')
    try:
        contacts=paginator.page(page)
    except PageNotAnInteger:
        contacts=paginator.page(1)
    except EmptyPage:
        contacts=paginator.page(paginator.num_pages)
    return  render(request,"event_manage.html",{"user":username,"events":contacts})

#嘉宾管理
@login_required
def guest_manage(request):
    username=request.session.get('user','')
    guest_list= Guest.objects.all()
    paginator=Paginator(guest_list,2)
    page=request.GET.get('page')
    try:
        contacts=paginator.page(page)
    except PageNotAnInteger:
        #If page is not an integer,deliver first page.
        contacts =paginator.page(1)
    except EmptyPage:
        #If page is out of range (e.g. 9999),deliver last page of results.
        contacts=paginator.page(paginator.num_pages)
    return render(request,"guest_manage.html",{"user":username,"guests":contacts})

#签到页面
@login_required
def sign_index(request,event_id):
    event=get_object_or_404(Event,id=event_id)
    sign_people=Guest.objects.filter(event_id=event_id,sign=1).count
    total_people=Guest.objects.filter(event_id=event_id).count

    return render(request,'sign_index.html',{'event':event,'sign_people':sign_people,'total_people':total_people})

#签到功能
#@login_required
def sign_index_action(request,event_id):
    event=get_object_or_404(Event,id=event_id)
    phone=request.POST.get('phone','')
    sign_people=Guest.objects.filter(event_id=event_id,sign=1).count
    total_people=Guest.objects.filter(event_id=event_id).count

    result=Guest.objects.filter(phone=phone)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'phone error.',
                                                 'sign_people':sign_people,'total_people':total_people})

    result=Guest.objects.filter(event_id=event_id,phone=phone)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'event id or phone error.',
                                                 'sign_people':sign_people,'total_people':total_people})

    result=Guest.objects.get(event=event_id,phone=phone)
    if result.sign:
        return render(request,'sign_index.html',{'event':event,'hint':'user has sign in.',
                                                 'sign_people':sign_people,'total_people':total_people})

    else:
        Guest.objects.filter(event_id=event_id,phone=phone).update(sign='1')
        return render(request,'sign_index.html',{'event':event,'hint':'sign in success.','guest':result,
                                                 'sign_people':sign_people,'total_people':total_people})

#退出功能
@login_required
def logout(request):
    auth.logout(request)
    response=HttpResponseRedirect('/index/')
    return response