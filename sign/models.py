#coding=utf-8
from __future__ import unicode_literals
import django.utils.timezone as timezone
from django.db import models
import datetime

# Create your models here.

class Event(models.Model):
    name=models.CharField(max_length=100)
    limit=models.IntegerField()
    status=models.BooleanField()
    address=models.CharField(max_length=200)
    start_time=models.DateTimeField('event time')
    creat_time=models.DateTimeField(auto_now=True)

    def  __str__(self):
        return self.name


class Guest(models.Model):
    event=models.ForeignKey(Event)
    realname=models.CharField(max_length=64)
    phone=models.CharField(max_length=16)
    email=models.EmailField()
    sign=models.BooleanField()
    creat_time=models.DateTimeField(auto_now=True)
    class Meta:
        unique_together=("event","phone")
    def __str__(self):
        return self.realname

# 修改创建时间类型
#ALTER TABLE  `sign_event` CHANGE  `creat_time`  `creat_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
#ALTER TABLE  `sign_guest` CHANGE  `creat_time`  `creat_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP