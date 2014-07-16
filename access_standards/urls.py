#-*-  coding:utf-8  -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'access_standards.views.index', name='index'),
    url(r'^standard/$', 'access_standards.views.standard'),
)
