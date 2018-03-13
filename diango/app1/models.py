from django.db import models
from django.utils import timezone

class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=60)
    pwd = models.CharField(max_length=60)
    nicheng = models.CharField(unique=True, max_length=60, blank=True, null=True)
    updtime = models.DateTimeField(blank=True, null=True)
    role = models.IntegerField(default=1)
    msgnum = models.IntegerField(default=0)
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

class Writers(models.Model):
    id = models.BigIntegerField(primary_key=True)
    realname = models.CharField(max_length=60)
    idnumber = models.CharField(unique=True, max_length=60)
    telnumber = models.IntegerField(unique=True)
    qq = models.CharField(max_length=60, blank=True, null=True)
    biming = models.CharField(unique=True, max_length=60)
    idimage = models.CharField(max_length=60)
    idperson = models.CharField(max_length=60)
    appexplain = models.CharField(max_length=255)
    updtime = models.DateTimeField()
    createtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'writers'

class Works(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.BigIntegerField()
    workname = models.CharField(max_length=60)
    typeoneid = models.BigIntegerField()
    typetwoid = models.BigIntegerField()
    label = models.CharField(max_length=60)
    licensetype = models.IntegerField()
    introduce = models.CharField(max_length=300)
    firstmsg = models.CharField(max_length=300)
    chaptenum = models.IntegerField(default=0)
    curchapte = models.BigIntegerField(default=0)
    pubflag = models.SmallIntegerField(default=0)
    finishflag = models.SmallIntegerField(default=0)
    cnum = models.IntegerField(default=0)
    updtime = models.DateTimeField()
    createtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'works'


class Worktypeone(models.Model):
    id = models.BigAutoField(primary_key=True)
    typename = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'worktypeone'


class Worktypetwo(models.Model):
    id = models.BigAutoField(primary_key=True)
    typename = models.CharField(max_length=60)
    oneid = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'worktypetwo'


class Chapters(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.BigIntegerField()
    worksid = models.BigIntegerField()
    chaptername = models.CharField(max_length=240)
    content = models.TextField(blank=True, null=True)
    pubflag = models.IntegerField(blank=True, null=True)
    updtime = models.DateTimeField()
    createtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'chapters'

class Msgs(models.Model):
    id = models.BigAutoField(primary_key=True)
    sendid = models.BigIntegerField()
    sendname = models.CharField(max_length=60)
    receiveid = models.BigIntegerField()
    content = models.CharField(max_length=300)
    createtime = models.DateTimeField()
    readflag = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'msgs'

class Myreading(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.BigIntegerField()
    workname = models.CharField(max_length=60)
    updatetime = models.DateTimeField()
    createtime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'myreading'
