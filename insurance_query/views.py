from django.views.generic import FormView
from ajaxres import AjaxResponseMixin


class InsuranceQuery2(FormView, AjaxResponseMixin):
    pass
