from django.conf.urls import patterns, url
from insurance_query.views import InsuranceQuery2


urlpatterns = patterns('',
    url(r'^2/$', InsuranceQuery2.as_view()),
)