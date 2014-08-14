# -*- coding: utf-8 -*-
from django.db import models


class City(models.Model):

    name = models.CharField(max_length=40)
    pinyin = models.CharField(max_length=20)
    parent = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'city'


class CarInfo(models.Model):

    license_plate_num = models.CharField(max_length=7, null=True, blank=True, unique=True, verbose_name=u'车牌号')
    engine_no = models.CharField(max_length=6, null=True, blank=True, verbose_name=u'发动机号')
    VIN_last_six = models.CharField(max_length=6, null=True, blank=True, verbose_name=u'车架号后6位')
    VIN = models.CharField(max_length=17, null=True, blank=True, verbose_name=u'车架号')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    class Meta:
        db_table = 'car_info'
        verbose_name_plural = u'车辆信息'


class ViolationRecord(models.Model):

    car_info = models.ForeignKey(CarInfo, db_column='car_info')
    area = models.CharField(max_length=50)
    money = models.IntegerField()
    chuli = models.CharField(max_length=10)
    fen = models.IntegerField()
    date = models.CharField(max_length=20)
    act = models.CharField(max_length=100)

    class Meta:
        db_table = 'violation_record'
