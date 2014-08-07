from django.conf.urls import patterns, url
from insurance_query.views import PostQueryInsurance


urlpatterns = patterns('',
    url(r'^$', PostQueryInsurance.as_view()),
)