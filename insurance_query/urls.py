from django.conf.urls import patterns, url
from insurance_query.views import InsuranceQuery


urlpatterns = patterns('',
    url(r'^$', InsuranceQuery.as_view()),
)