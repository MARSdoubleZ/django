from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db.models import F
import MySQLdb
import time
import datetime
import os
from django.db import transaction
from app1.models import Writers
from app1.models import Users
from app1.models import Msgs
from bson.objectid import ObjectId

import pymongo

def index(request):
    try:
        loginbean = request.session['loginbean']
        if loginbean == None:
            return HttpResponse("<script>alert('登录过期,请重新登录');location.href='/';</script>")
        if loginbean['role'] == 0:
            return render(request, 'admin/adminhome.html', {'loginbean': loginbean})
        else:
            return HttpResponse("<script>alert('您无权限进入');location.href='/;</script>")
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('请登录');location.href='/';</script>")


def writerApplyList(request):
    try:
        loginbean = request.session['loginbean']
        if loginbean == None:
            return HttpResponse("<script>alert('登录过期,请重新登录');location.href='/';</script>")
        if loginbean['role'] == 0:
            sql = 'select u.id,w.realname,w.biming,w.updtime from users u,writers w where u.role=2 and u.id=w.id';
            rs = Users.objects.raw(sql)
            # print(rs[0].realname)
            # print('------------------')
            # for row in rs:
            #         print(row.realname)

            return render(request, 'admin/writerApplyList.html', {'loginbean': loginbean, 'rs': rs})
        else:
            return HttpResponse("<script>alert('您无权限进入');location.href='/;</script>")
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('请登录');location.href='/';</script>")


def applyInfo(request):
    try:
        loginbean = request.session['loginbean']
        if loginbean == None:
            return HttpResponse("<script>alert('登陆过期，请重新登陆');location.href='/';</script>")
        if loginbean['role'] == 0:
            id = request.GET.get('id')
            rs = Writers.objects.filter(id=id).first()
            return render(request, 'admin/applyInfo.html', {'loginbean': loginbean, 'rs': rs, 'id': id})
        else:
            return HttpResponse("<script>alert('您无权限进入');location.href='/;</script>")
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('请登录');location.href='/';</script>")


def applyPass(request):
    try:
        loginbean = request.session['loginbean']
        if loginbean == None:
            return HttpResponse("<script>alert('登录过期,请重新登录');location.href='/';</script>")
        if loginbean['role'] == 0:
            id = request.GET.get('id')
            transaction.set_autocommit(False)
            try:

                Users.objects.filter(id=id).update(role=3,msgnum= F('msgnum') + 1)
                dict = {}
                dict['sendid'] = loginbean['id']
                dict['sendname'] = '系统通知'
                dict['receiveid'] = id
                dict['content'] = '您的作家申请已通过'
                dict['createtime']=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                msg = Msgs.objects.create(**dict)
                transaction.commit()
            except:
                transaction.rollback()
            finally:
                transaction.set_autocommit(True)
            return redirect('/writerapplylist')

            # rs = Writers.objects.filter(id=id).first()
            # return render(request, 'admin/applyInfo.html', {'loginbean': loginbean,'rs':rs,'id':id})
        else:
            return HttpResponse("<script>alert('您无权限进入');location.href='/;</script>")
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('请登录');location.href='/';</script>")


def applyRefuse(request):
    try:
        loginbean = request.session['loginbean']
        if loginbean == None:
            return HttpResponse("<script>alert('登录过期,请重新登录');location.href='/';</script>")
        if loginbean['role'] == 0:
            if request.method == 'POST':
                id = request.POST.get('receiveid')
                content = request.POST.get('content')
                transaction.set_autocommit(False)
                try:
                    Users.objects.filter(id=id).update(role=1, msgnum=F('msgnum') + 1)
                    Writers.objects.filter(id=id).delete()
                    dict = {}
                    dict['sendid'] = loginbean['id']
                    dict['sendname'] = '系统通知'
                    dict['receiveid'] = id
                    dict['content'] = '您的审核申请未通过,原因:%s,请修改后重新申请' % (content)
                    dict['createtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    msg = Msgs.objects.create(**dict)
                    # print(dir(transaction))
                    transaction.commit()
                except:
                    transaction.rollback()
                finally:
                    transaction.set_autocommit(True)
                return redirect('/writerapplylist')
            else:
                return HttpResponse("<script>alert('错误的提交方式');location.href='/;</script>")
        else:
            return HttpResponse("<script>alert('您无权限进入');location.href='/;</script>")
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('请登录');location.href='/';</script>")

def worksClass(request):
    try:
        loginbean = request.session['loginbean']
        if loginbean == None:
            return HttpResponse("<script>alert('登录过期,请重新登录');location.href='/';</script>")
        if loginbean['role'] == 0:
            client = pymongo.MongoClient(host="192.168.60.13")
            dict = {}
            db = client.novel
            collection = db.novelclass
            rs = collection.find({})
            rsObj = {}
            for item in rs:
                item['id']=item['_id']

                if item['pid']==None:
                    rsObj[item['_id']]=[item]
                else:
                    rsObj[ObjectId(item['pid'])].append(item)
            # return render(request, 'admin/worksClass.html', {'loginbean': loginbean,'rs': rsObj})
            return render(request, 'admin/worksClass.html', {'loginbean': loginbean,'rs': rsObj})
        else:
            return HttpResponse("<script>alert('您无权限进入');location.href='/;</script>")
    #
    except Exception as err:
        print(err)
        return HttpResponse("<script>alert('请登录');location.href='/';</script>")