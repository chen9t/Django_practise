from django.conf.urls import patterns, url
from insurance_query.views import PostInsuranceQueryView


urlpatterns = patterns('',
    url(r'^$', PostInsuranceQueryView.as_view()),
)