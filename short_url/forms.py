# -*- coding:utf-8 -*-
from django import forms


class LongUrlForm(forms.Form):

    url_long = forms.URLField(required=True,
            error_messages={
                'required': u'请输入URL',
                'invalid': u'请输入正确的URL'
            })
