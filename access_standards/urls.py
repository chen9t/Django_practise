#-*-  coding:utf-8  -*-
from django.conf.urls import patterns, url
from access_standards.views import AboutView, CityView


urlpatterns = patterns('',
    # url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    url(r'^about/$', AboutView.as_view()),
    url(r'^city/$', CityView.as_view()),
    url(r'^$', 'access_standards.views.index', name='index'),
)
