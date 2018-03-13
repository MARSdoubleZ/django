from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import MySQLdb
import time
import datetime
import os
from app1.models import Writers
from app1.models import Users
from app1.models import Works
from app1.models import Chapters


def deco(func):
    def _deco(request):
        reqFun = None
        try:
            loginbean = request.session['loginbean']
            if loginbean == None:
                return HttpResponse("<script>alert('登录过期,请重新登录');location.href='/';</script>")
            if loginbean['role'] == 3:
                reqFun = func(request, loginbean)
                return reqFun
                # return render(request, 'works/showCreateWorks.html', {'loginbean': loginbean})
            else:
                return HttpResponse("<script>alert('您无权限进入');location.href='/';</script>")
        except Exception as err:
            print(err)
            return HttpResponse("<script>alert('请登录');location.href='/';</script>")

    return _deco


@deco
def myworks(request, loginbean):
    rs = Works.objects.filter(uid=loginbean['id'])
    return render(request, 'works/myworks.html', {'loginbean': loginbean, 'rs': rs})


@deco
def showcreateworks(request, loginbean):
    return render(request, 'works/showCreateWorks.html', {'loginbean': loginbean})


@deco
def createworks(request, loginbean):
    if request.method == 'POST':
        dict = request.POST.dict()  # 转成字典形式
        try:
            del dict['csrfmiddlewaretoken']
            dict['uid'] = loginbean['id']
            works = Works.objects.create(createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                         **dict)  # **dict必须放到最后
            return redirect('/myworks')
        except Exception as err:
            print(err)
            errStr = err.args[1]
            print(errStr)
            return HttpResponse("数据库异常,稍后再试");
    else:
        return HttpResponse('请正确提交')


@deco
def worksmanage(request, loginbean):
    worksid = request.GET.get('worksid')
    rs = Chapters.objects.filter(worksid=worksid, uid=loginbean['id'])
    return render(request, 'works/worksmanage.html', {'loginbean': loginbean, 'rs': rs, 'worksid': worksid})


@deco
def createChapter(request, loginbean):
    if request.method == 'POST':
        dict = request.POST.dict()  # 转成字典形式
        try:
            del dict['csrfmiddlewaretoken']
            dict['uid'] = loginbean['id']
            chapter = Chapters.objects.create(createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                         **dict)  # **dict必须放到最后
            return redirect('/worksmanage?worksid=%s'%(dict['worksid']))
        except Exception as err:
            print(err)
            errStr = err.args[1]
            print(errStr)
            return HttpResponse("数据库异常,稍后再试");
    else:
        return HttpResponse('请正确提交')


@deco
def editChapter(request, loginbean):
    chapterid = request.GET.get('chapterid')
    rs = Chapters.objects.filter(id=chapterid, uid=loginbean['id'])

    return render(request, 'works/editChapter.html', {'loginbean': loginbean,'rs':rs})


@deco
def saveChapter(request,loginbean):
    if request.method == 'POST':
        dict = request.POST.dict()
        try:
            del dict['csrfmiddlewaretoken']
            chapter = Chapters.objects.filter(id=dict['chapterid'],uid=loginbean['id'])
            del dict['chapterid']
            chapter.update(**dict)
            return HttpResponse("编辑完成");
        except Exception as err:
            print(err)
            errStr = err.args[1]
            print(errStr)
            return HttpResponse("数据库异常，稍后再试");
    else:
         return HttpResponse('请正确提交')