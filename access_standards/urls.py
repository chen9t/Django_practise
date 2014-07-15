#-*-  coding:utf-8  -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView, ListView
from access_standards.models import AccessStandard


urlpatterns = patterns('',
    url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    url(r'^standard/$', ListView.as_view(model=AccessStandard, context_object_name='standard_list', template_name='standard_list.html')),
    url(r'^$', 'access_standards.views.index', name='index'),
)
