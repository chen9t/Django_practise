# -*- coding: utf-8 -*-

from django.views.generic import View, FormView, RedirectView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

from short_url import ShortURL
from short_url.forms import LongUrlForm
from short_url.models import ShortURLMap

from json_response import JsonResponseMixin
from short_url_settings import DOMAIN_NAME

__all__ = [
    'GetExpandURLView',
    'GetClicksView',
    'PostAchieveShortURLView',
    'ShortURLRedirectView',
]


class PostAchieveShortURLView(FormView, JsonResponseMixin):
    '''Generate short url from long url

    Request method: POST
    Parameters: POST parameters
    - url_long: Long url need to be converted into short url.
    '''

    http_method_names = ['post', ]
    form_class = LongUrlForm
    err_msg = {
        'fail_to_generate': u'生成短链接失败'
    }

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        context = {}
        url_long = form.cleaned_data['url_long']
        surl_generator = ShortURL(url_long)
        # try:
        #     short_path = surl_generator.get_short_url()
        # except:
        #     self.update_errors(self.err_msg['fail_to_generate'])
        # else:
        #     url_short = ''.join([DOMAIN_NAME, short_path])
        #     context.update({
        #         'url_short': url_short
        #     })
        short_path = surl_generator.get_short_url()
        url_short = ''.join([DOMAIN_NAME, short_path])
        context.update({
            'url_short': url_short
        })

        return self.json_response(context)

    def form_invalid(self, form):
        self.update_errors(form.errors.popitem()[-1][0])
        return self.json_response()


class GetExpandURLView(View, JsonResponseMixin):
    '''Expand short url into long url

    Request method: GET
    - url_short: short url need to be analyzed.
    '''

    http_method_names = ['get', ]
    err_msg = {
        'fail_to_get': u'返回长链接失败',
        'no_short_url': u'请输入需要解析的短链接',
        'url_not_exist': u'无法解析该短链接',
    }

    def get(self, request, *args, **kwargs):
        context = {}
        url_short = request.GET.get('url_short', '')
        if url_short:
            try:
                url_long = ShortURL.get_long_url(url_short)
            except:
                self.update_errors(self.err_msg['fail_to_get'])
            else:
                if url_long:
                    context.update({'url_long': url_long})
                else:
                    self.update_errors(self.err_msg['url_not_exist'])
        else:
            self.update_errors(self.err_msg['no_short_url'])

        return self.json_response(context)


class GetClicksView(View, JsonResponseMixin):
    '''Count clicks of the short url

    Request method: GET
    - url_short: Get clicks of the short url.
    '''
    http_method_names = ['get', ]
    err_msg = {
        'fail_to_get': u'返回点击数失败',
        'no_short_url': u'请输入需要查询的短链接',
        'url_not_exist': u'无法获取该链接的点击数',
    }

    def get(self, request, *args, **kwargs):
        context = {}
        url_short = request.GET.get('url_short', '')
        if url_short:
            try:
                count = ShortURL.get_clicks(url_short)
            except:
                self.update_errors(self.err_msg['fail_to_get'])
            if count >= 0:
                context.update({
                    'count': count
                    })
            else:
                self.update_errors(self.err_msg['url_not_exist'])
        else:
            self.update_errors(self.err_msg['no_short_url'])

        return self.json_response(context)


class ShortURLRedirectView(RedirectView):
    ''' Redirect short url to long url.'''

    http_method_names = ['get', ]
    permanent = False

    def get_redirect_url(self, **kwargs):
        short_url = kwargs.get('short_url', '')
        long_url = '/'
        if short_url:
            url = ShortURL.get_long_url(short_url)
            if url:
                try:
                    ShortURLMap.objects.filter(url_long=url).\
                        update(clicks=F('clicks') + 1)
                except:
                    pass
                long_url = url
        return long_url
