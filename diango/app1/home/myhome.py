from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
import MySQLdb
import time
import datetime
import os
from app1.models import Writers
from app1.models import Users
from app1.models import Msgs


def index(request):
    # return HttpResponse("Hello 世界")
    try:
        loginbean = request.session['loginbean']
        if loginbean == None:
            return HttpResponse("<script>alert('登录过期,请重新登录');location.href='/';</script>")
        if loginbean['role'] > 0:
            # print(loginbean)
            return render(request, 'home/myhome.html', {'loginbean': loginbean})
        else:
            return HttpResponse("<script>alert('您无权限进入');location.href='/';</script>")
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('网页错误');location.href='/';</script>")

def msgs(request):
    try:
        loginbean = request.session['loginbean']
        if loginbean==None:
            return HttpResponse("<script>alert('登录过期,请重新登录');location.href='/';</script>")
        if loginbean['role']>0:
            rs = Msgs.objects.filter(receiveid=loginbean['id'])
            Users.objects.filter(id=loginbean['id']).update(msgnum=0)
            loginbean['msgnum']=0
            request.session['loginbean']=loginbean
            return render(request, 'home/msgs.html',{'loginbean':loginbean,'rs':rs})
        else:
            return HttpResponse("<script>alert('您无权限进入');location.href='/';</script>")
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('请登录');location.href='/';</script>")

def writerApply(request):
    try:

        loginbean = request.session['loginbean']
        if loginbean == None:
            return HttpResponse("<script>alert('登录过期,请重新登录');location.href='/';</script>")

        if request.method != 'POST':
            return render(request, 'home/writerApply.html')
        else:
            dict = request.POST.dict()
            print(dict)
            del dict['csrfmiddlewaretoken']
            idimage = request.FILES.get('idimage')
            if idimage == None:
                return HttpResponse('必须上传身份证照片')
                exit(0)
            idperson = request.FILES.get('idperson')
            if idperson == None:
                return HttpResponse('必须上传手持身份证照片')
                exit(0)
            try:
                # 改图片名字另存为
                idimagePath = "%s1%s" % (time.time(), idimage.name)
                f = open(os.path.join("app1\\static\\images", idimagePath), 'wb')
                for chunk in idimage.chunks(chunk_size=1024):
                    f.write(chunk)
                dict['idimage'] = idimagePath
                idpersonPath = "%s2%s" % (time.time(), idperson.name)
                f = open(os.path.join("app1\\static\\images", idpersonPath), 'wb')
                for chunk in idperson.chunks(chunk_size=1024):
                    f.write(chunk)
                dict['idperson'] = idpersonPath
                dict["id"] = loginbean['id']
                writer = Writers.objects.create(
                    createtime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), **dict)
                Users.objects.filter(id=loginbean['id']).update(role=2)
                loginbean['role'] = 2
                request.session['loginbean'] = loginbean

            except Exception as e:
                print(e)
            finally:
                f.close()
                return HttpResponse('提交成功')

    except Exception as err:
        print("%^&*()_")
        print(err)
        return HttpResponse("<script>alert('网页错误');</script>")
