# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

from short_url.views import GetExpandURLView
from short_url.views import GetClicksView
from short_url.views import PostAchieveShortURLView


urlpatterns = patterns('',

    url(r'^shorten$', PostAchieveShortURLView.as_view()),
    url(r'^expand', GetExpandURLView.as_view()),
    url(r'^clicks', GetClicksView.as_view()),
)
