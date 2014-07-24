#-*-  coding:utf-8  -*-
from django.conf.urls import patterns, url
from vehicle_violation_query.views import ViolationQuery


urlpatterns = patterns('',
    url(r'^$', ViolationQuery.as_view()),
)