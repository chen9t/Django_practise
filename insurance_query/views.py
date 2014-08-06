from django.views.generic import FormView
from ajaxres import AjaxResponseMixin


class InsuranceQuery(FormView, AjaxResponseMixin):
    pass
