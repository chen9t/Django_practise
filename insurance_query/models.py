# -*- coding: utf-8 -*-
from django.db import models
from vehicle_violation_query.models import CarInfo


class InsuranceInfo(models.Model):

    LicenseNo = models.ForeignKey(CarInfo, db_column='car_info', verbose_name=u'车辆信息')
    ClaimStatus = models.CharField(max_length=5, verbose_name=u'案件状态')
    ClaimQueryNo = models.CharField(max_length=50, verbose_name=u'理赔编码')
    PolicyNo = models.CharField(max_length=30, null=True, blank=True, verbose_name=u'保单号')
    OperateDate = models.DateField(null=True, blank=True, verbose_name=u'签单时间')
    StartDate = models.DateField(null=True, blank=True, verbose_name=u'起保时间')
    EndDate = models.DateField(null=True, blank=True, verbose_name=u'终保时间')

    CompanyCode = models.CharField(max_length=40, null=True, blank=True, verbose_name=u'承保公司')
    EstimateLoss = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=u'赔款金额')

    DamageDate = models.DateField(null=True, blank=True, verbose_name=u'出险时间')
    ReportDate = models.DateField(null=True, blank=True, verbose_name=u'报案时间')
    ClaimDate = models.DateField(null=True, blank=True, verbose_name=u'立案时间')
    EndcaseDate = models.DateField(null=True, blank=True, verbose_name=u'结案时间')

    RiskType = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'险种类型')
    DriverName = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'损害赔偿责任人')
    SumPaid = models.CharField(max_length=10, null=True, blank=True, verbose_name=u'总付款')
    IndemnityDuty = models.CharField(max_length=50, null=True, blank=True, verbose_name=u'赔偿责任')

    created_on = models.DateTimeField(auto_now_add=True, auto_now=True, verbose_name=u'创建时间')


    class Meta:
        db_table = 'insurance_info'
        verbose_name_plural = u'出险记录'
