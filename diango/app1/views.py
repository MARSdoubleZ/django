from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Users
from datetime import time
from datetime import datetime
from django.contrib.sessions.backends.db import SessionStore
import MySQLdb
from app1.models import Works
from app1.models import Chapters
from app1.models import Myreading

def index(request):

    loginBean = None
    try:
      rs = Works.objects.filter()
      ro = Chapters.objects.filter()
      return render(request, 'index.html', {'loginbean': loginBean, 'rs': rs, 'ro': ro})
    except Exception as err:
        pass

def myRead(request,loginbean):
    try:
        loginbean = request.session['loginbean']
        if loginbean==None:
            return HttpResponse("<script>alert('登录过期,请重新登录');location.href='/';</script>")
        if loginbean['role']>0:
            rs = Myreading.objects.filter(uid=loginbean['id'])
            myread = Myreading.objects.create(
                createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), **dict)

            request.session['loginbean']=loginbean
            return render(request, 'home/myreading.html',{'loginbean':loginbean,'rs':rs})
        else:
            return HttpResponse("<script>alert('您无权限进入');location.href='/';</script>")
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('请登录');location.href='/';</script>")

def homeHead(request):
    return render(request, 'home/homeHead.html')


def myhome(request):
    return render(request, 'home/myhome.html')


def reg(request):
    # 判断是否POST方式，如果是则进行下面的表单处理
    if request.method == 'POST':
        dict = request.POST.dict()

        try:

            del dict['csrfmiddlewaretoken']

            # row = Users.objects.create(createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            #                      **userDict)  # **dict必须放到最后

            # 格式化时间
            myDate = datetime.now()
            formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S")

            # 第一步，保存新用户信息到数据库
            row = Users.objects.create(createtime=formatedDate, **dict)  # **dict必须放到最后

            # Users.objects.create(email=email, pwd=pwd, nicheng=nicheng)  # 创建一个对象实例


            # 第二步，如果验证通过，则保存用户信息到 session, 实现用户登陆

            dict['id'] = row.id
            # Users.objects.create(email=email, pwd=pwd, nicheng=nicheng) #创建一个对象实例
            request.session['dict'] = dict
            return redirect('/')
        except Exception as err:
            errStr = err.args[1]
            if 'emailuniq' in errStr:
                return HttpResponse('<script>alert("用户名重复");location.href="/";</script>')
            elif 'nichenguniq' in errStr:
                return HttpResponse('<script>alert("昵称重复");location.href="/";</script>')

    else:
        return HttpResponse('请正确提交')


def login(request):
    if request.method == 'POST':

        emailVal = request.POST.get('email')
        pwd = request.POST.get('pwd')

        row = Users.objects.filter(email=emailVal, pwd=pwd).first()

        if row != None:
            loginbean = {}
            loginbean['id'] = row.id
            loginbean['nicheng'] = row.nicheng
            loginbean['role'] = row.role
            loginbean['msgnum'] = row.msgnum
            request.session['loginbean'] = loginbean
            # return HttpResponse('登录成功')
            if row.role>0:
                return redirect('/home')
            else:
                return redirect('/adminhome')
        else:
            return HttpResponse('用户名/密码错误')
    else:
        dict = request.session['dict']
        if dict != None:
            loginbean = {}
            loginbean['id'] = dict['id']
            loginbean['nicheng'] = dict['nicheng']
            loginbean['role'] = 1
            request.session['loginbean'] = loginbean
            del request.session['dict']
            # return HttpResponse('登录成功')
            return redirect('/')
        else:
            return HttpResponse('请登录')
            # return HttpResponse(rs)


def dengchu(request):
    del request.session['loginbean']

    return redirect('/')






