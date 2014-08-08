# -*- coding: utf-8 -*-
from requests.exceptions import Timeout, HTTPError

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from insurance_query.forms import QueryInfoForm

from insurance_query import GetXMLResponse
from insurance_query import ParseXML

from ajaxres import AjaxResponseMixin


class PostQueryInsurance(FormView, AjaxResponseMixin):
    
    http_method_names = ['post', ]
    form_class = QueryInfoForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):        
        context = {}

        query_type = form.cleaned_data['query_type']
        kwargs = form.cleaned_data
        kwargs.pop('query_type')

        # First request, get the total pages
        try:
            xml_info = self.get_response(query_type, **kwargs)
        except Timeout:
            self.update_errors(self.err_msg['time_out'])
        except HTTPError:
            self.update_errors(self.err_msg['request_failure'])

        # If the info is currect at the first request, don't need to check it again.
        record_list = []
        total_page = 1
        if xml_info.error:
            self.update_errors(xml_info.error[-1])
        else:
            record_list.extend(xml_info.elems)
            total_page = xml_info.totalpage

        # The following requests mean to get the rest records.
        if total_page > 1:
            for page in xrange(2, total_page + 1):
                kwargs.update({'pageno': str(page)})
                try:
                    xml_info = self.get_response(query_type, **kwargs)
                except Timeout:
                    self.update_errors(self.err_msg['time_out'])
                    break
                except HTTPError:
                    self.update_errors(self.err_msg['request_failure'])
                    break
                else:
                    record_list.extend(xml_info.elems)
         
        context.update({'records': record_list})

        return self.ajax_response(context)

    def form_invalid(self, form):
        self.update_errors(form.errors.popitem()[-1][0])
        return self.ajax_response()

    def get_response(self, query_type, **kwargs):

        xml_res = GetXMLResponse(query_type, **kwargs)

        try:
            xml_stream = xml_res.get_xml_stream()
        except Timeout:
            raise Timeout
        except HTTPError:
            raise HTTPError

        xml_info = ParseXML(xml_stream)
        return xml_info
