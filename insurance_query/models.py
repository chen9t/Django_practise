# -*- coding: utf-8 -*-
from django.db import models

class CarInfo(models.Model):

    license_no = models.CharField(max_length=7, unique=True, verbose_name=u'车牌号')
    frame_last_six_no = models.CharField(max_length=6, verbose_name=u'车架号后6位')
    # engine_last_six_no = models.CharField(max_length=6, verbose_name=u'发动机号后6位')
    # frame_no = models.CharField(max_length=17, unique=True, verbose_name=u'车架号')

    class Meta:
        db_table = 'car'

    def __unicode__(self):
        return self.license_no

class InsuranceInfo(models.Model):

    #     PolicyNo[M]         保单号
    #     OperateDate[M]      签单时间
    #     StartDate[M]        起保时间
    #     EndDate[M]          终保时间
    #     LicenseNo[M]        车牌号
    #     CompanyCode[M]      承保公司
    #     RiskType[M]         险种类型

    #     ClaimStatus[O]      案件状态
    #     ClaimQueryNo[O]     理赔编码
    #     EstimateLoss[O]     赔款金额
    #     SumPaid[O]          总付款
    #     DamageDate[O]       出险时间
    #     ReportDate[O]       报案时间
    #     ClaimDate[O]        立案时间
    #     EndcaseDate[O]      结案时间
    #     DriverName[O]       损害赔偿责任

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


    class Meta:
        db_table = 'insurance_info'

    def __unicode__(self):
        return self.claim_query_no
