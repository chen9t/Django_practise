# -*- coding: utf-8 -*-
import threading

from requests.exceptions import Timeout, HTTPError

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView

from insurance_query.forms import InsuranceQueryForm

from insurance_query import GetXMLResponse
from insurance_query import ParseXML
from insurance_query import StoreInfo

from ajaxres import AjaxResponseMixin


class PostInsuranceQueryView(FormView, AjaxResponseMixin):
    ''' POST insurance query.

    Request method: POST
    - query_type : 2
        - license_no : license no.
        - VIN_last_six : the last six no of VIN.
    - query_type : 4
        - VIN : Vehicle Identification Number.
    '''

    http_method_names = ['post', ]
    form_class = InsuranceQueryForm

    err_msg = {
        'time_out': u'请求超时',
        'request_failure': u'请求失败',
    }

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):        
        context = {}
        record_list = []

        query_type = form.cleaned_data['query_type']
        kwargs = form.cleaned_data
        kwargs.pop('query_type')

        # First request, get the total pages.
        try:
            xml_info = self.get_response(query_type, **kwargs)
        except Timeout:
            self.update_errors(self.err_msg['time_out'])
        except HTTPError:
            self.update_errors(self.err_msg['request_failure'])
        else:
            if xml_info.error:
                self.update_errors(xml_info.error[-1])
            else:
                total_page = xml_info.totalpage
                # The following requests mean to get all records.
                for page in xrange(1, total_page + 1):
                    kwargs.update({'pageno': str(page)})
                    try:
                        xml_info = self.get_response(query_type, **kwargs)
                    except Timeout:
                        self.update_errors(self.err_msg['time_out'])
                        break
                    except HTTPError:
                        self.update_errors(self.err_msg['request_failure'])
                        break
                    if xml_info.error:
                        self.update_errors(xml_info.error[-1])
                        break
                    else:
                        record_list.extend(xml_info.elems)
                else:
                    # If only get all records at a time, return the record list. Otherwise, return a blank list.
                    # For the reason that, any request in the loop above may get errors. When it happens, we should
                    # return error messgaes rather than part of the records we already got.
                    if query_type == 'by_licenseno_VIN':
                        new_thread = threading.Thread(target=self.store_info, args=(query_type, record_list, kwargs))
                        new_thread.start()
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
            raise
        except HTTPError:
            raise

        xml_info = ParseXML(xml_stream)
        return xml_info

    def store_info(self, query_type, record_list, kwargs):
            info_storage = StoreInfo(query_type, **kwargs)
            # Store car info.
            car_info, car_not_exists =  info_storage.store_car_info1()
            # Store insurance records.
            info_storage.store_insurance_info(car_info, car_not_exists, record_list)
