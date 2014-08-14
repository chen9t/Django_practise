# -*- coding: utf-8 -*-
from django.conf import settings


SERVICE_URL = getattr(settings, 'SERVICE_URL', "http://106.37.176.173:9080/phoneserver/phserver")
TIME_OUT = getattr(settings, 'TIME_OUT', 10)

QUERY_TYPE = {
    'by_policeno' : '1', # 根据保单号查询
    'by_licenseno_VIN' : '2', # 根据车牌号和车架号后六位查询
    'by_VIN_engineno' : '3', # 根据车架号后六位和发动机号后六位查询
    'by_VIN' : '4', # 根据车架号查询
}
