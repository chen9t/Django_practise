#-*-  coding:utf-8  -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'vehicle_violation_query.views.query'),
)