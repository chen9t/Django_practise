#-*- coding:utf-8 -*-
from django.db import models


class AccessStandard(models.Model):
    city = models.CharField(max_length=40, unique=True, verbose_name=u'城市')
    emission_standard = models.CharField(max_length=20, null=True, verbose_name=u'排放标准')
    standard_details = models.CharField(max_length=100, null=True, verbose_name=u'标准细节')
    DVM = models.CharField(max_length=20, null=True, verbose_name=u'车 管 所')

    def __unicode__(self):
        return self.city

    class Meta:
        db_table = 'access_standard'
        app_label = u'准入标准管理'
        verbose_name_plural = u'准入标准信息'
