from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from app1 import views as core_views
from django.conf.urls import include
from . import views
from app1.home import myhome
from app1.home import adminHome
from . import common
from .home import works




urlpatterns = [
    url(r'^reg', views.reg, name='reg'),
    url(r'^$', views.index, name='index'),
    url(r'^login', views.login, name='login'),
    url(r'^dengchu', views.dengchu, name='dengchu'),
    url(r'^homeHead', views.homeHead, name='homeHead'),
    url(r'^writerApply', myhome.writerApply, name='writerApply'),
    # url(r'^home', views.myhome, name='myhome'),
    url(r'^home$', myhome.index),
    url(r'^adminhome$', adminHome.index),
    url(r'^writerapplylist$', adminHome.writerApplyList),
    url(r'^showImg$', common.showImg),
    url(r'^applyInfo',adminHome.applyInfo),
    url(r'^applyPass',adminHome.applyPass),
    url(r'^applyRefuse', adminHome.applyRefuse),
    url(r'^myworks/',works.myworks),
    url(r'^showcreateworks',works.showcreateworks),
    url(r'^createworks', works.createworks),
    url(r'^worksmanage', works.worksmanage),
    url(r'^createChapter', works.createChapter),
    url(r'^editChapter', works.editChapter),
    url(r'^saveChapter', works.saveChapter),
    url(r'^msgs', myhome.msgs),
    url(r'^myRead', views.myRead),
    url(r'^worksClass', adminHome.worksClass),


]
