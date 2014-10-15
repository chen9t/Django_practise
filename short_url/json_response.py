# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.utils import simplejson


HTTP_TIMEOUT = 4

class JsonResponseMixin(object):

    status = 'success'
    error_msg = 'message'

    def update_errors(self, msg, errors=None):
        # 更新错误信息
        self.status = 'error'
        if errors is not None:
            self.error_msg = errors
        else:
            self.error_msg = msg

    def ensure_dict(self, context):
        # 将获取到的数据转化为字典格式
        if context is None:
            context = {}
        if not isinstance(context, dict):
            context = {'data': context}

        return context

    def json_response(self, data=None, **kwargs):
        # 将获得的数据和状态数据打包成json返回
        data = self.ensure_dict(data)
        data.update(**kwargs)
        context = {
            'status': self.status,
            'msg': self.error_msg,
        }
        context.update(data)

        return HttpResponse(simplejson.dumps(context),
                            mimetype='application/json')
