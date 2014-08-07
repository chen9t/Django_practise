# -*- coding: utf-8 -*-
import re

from django import forms


class QueryInfoForm(forms.Form):

    QUERY_TYPE_CHOICES = (('1', '根据保单号查询'),
                                            ('2', '根据车牌号和车架号后六位查询'),
                                            ('3', '根据车架号后六位和发动机号后六位查询'),
                                            ('4', '根据车架号查询'))

    err_msg = {
        'no_policy_no': u'请输入保单号',
        'no_license_no': u'请输入车牌号',
        'no_frame_last_six_no': u'请输入车架号后6位',
        'no_engine_last_six_no': u'请输入发动机号后6位',
        'no_frame_no': u'请输入车架号',
        'wrong_policy_no': u'请输入正确的保单号',
        'wrong_license_no': u'请输入正确的车牌号',
        'wrong_frame_last_six_no': u'请输入正确的车架号后6位',
        'wrong_frame_no': u'请输入正确的车架号'
    }

    query_type = forms.ChoiceField(
        required=True,
        choices=QUERY_TYPE_CHOICES,
        error_messages={
            'required': u'请选择查询方式',
            'invalid_choice': '请选择正确的查询方式',
        })

    policy_no = forms.CharField(
        min_length=22,
        max_length=22,
        required=False,
        error_messages={
            'min_length': u'保单号过短',
            'max_length': u'保单号过长'
        })

    license_no = forms.CharField(
        min_length=7,
        max_length=7,
        required=False,
        error_messages={
            'min_length': u'车牌号过短',
            'max_length': u'车牌号过长'
        })

    frame_last_six_no = forms.CharField(
        min_length=6,
        max_length=6,
        required=False,
        error_messages={
            'min_length': u'车架号过短',
            'max_length': u'车架号过长'
        })

    engine_last_six_no = forms.CharField(
        min_length=6,
        max_length=6,
        required=False,
        error_messages={
            'min_length': u'发动机号过短',
            'max_length': u'发动机号过长'
        })

    frame_no = forms.CharField(
        min_length=17,
        max_length=17,
        required=False,
        error_messages={
            'min_length': u'车架号过短',
            'max_length': u'车架号过短'
        })

    # def clean_policy_no(self):
    #     policy_no = self.cleaned_data['policy_no']
    #     if not re.match(r'^[0-9A-Z]{22}', policy_no):
    #         raise forms.ValidationError(
    #             self.err_msg['wrong_policy_no'])
    #     return policy_no

    # def clean_license_no(self):
    #     license_no = self.cleaned_data['license_no']
    #     if not re.match(ur'^[京津沪渝冀豫云辽黑湘皖鲁苏赣浙粤鄂桂甘晋蒙陕吉闽贵青藏川宁新琼][A-Z][A-Z0-9]{5}', license_no):
    #         raise forms.ValidationError(
    #             self.err_msg['wrong_license_no'])
    #     return license_no

    # def clean_frame_last_six_no(self):
    #     frame_last_six_no = self.cleaned_data['frame_last_six_no']
    #     if not re.match(r'^[0-9A-Z]{6}', frame_last_six_no):
    #         raise forms.ValidationError(
    #             self.err_msg['wrong_frame_last_six_no'])
    #     return frame_last_six_no

    # def clean_frame_no(self):
    #     frame_no = self.cleaned_data['frame_no']
    #     if not re.match(r'^[0-9A-Z]{17}', frame_no):
    #         raise forms.ValidationError(
    #             self.err_msg['wrong_frame_no'])
    #     return frame_no

    def clean(self):
        print self.errors
        query_type = self.cleaned_data.get('query_type', '')

        if query_type == '1':
            policy_no = self.cleaned_data.get('policy_no', '')
            if not policy_no:
                raise forms.ValidationError(
                    self.err_msg['no_policy_no'])
            elif not re.match(r'^[0-9A-Z]{22}$', policy_no):
                raise forms.ValidationError(
                    self.err_msg['wrong_policy_no'])

        elif query_type == '2':
            license_no = self.cleaned_data.get('license_no', '')
            if not license_no:
                raise forms.ValidationError(
                    self.err_msg['no_license_no'])
            elif not re.match(ur'^[京津沪渝冀豫云辽黑湘皖鲁苏赣浙粤鄂桂甘晋蒙陕吉闽贵青藏川宁新琼][A-Z][A-Z0-9]{5}$', license_no):
                raise forms.ValidationError(
                    self.err_msg['wrong_license_no'])

            frame_last_six_no = self.cleaned_data.get('frame_last_six_no', '')
            if not frame_last_six_no:
                raise forms.ValidationError(
                    self.err_msg['no_frame_last_six_no'])
            elif not re.match(r'^[0-9A-Z]{6}$', frame_last_six_no):
                raise forms.ValidationError(
                    self.err_msg['wrong_frame_last_six_no'])

        elif query_type == '3':
            frame_last_six_no = self.cleaned_data.get('frame_last_six_no', '')
            if not frame_last_six_no:
                raise forms.ValidationError(
                    self.err_msg['no_frame_last_six_no'])
            elif not re.match(r'^[0-9A-Z]{6}$', frame_last_six_no):
                raise forms.ValidationError(
                    self.err_msg['wrong_frame_last_six_no'])

            engine_last_six_no = self.cleaned_data.get('engine_last_six_no', '')
            if not engine_last_six_no:
                raise forms.ValidationError(
                    self.err_msg['no_engine_last_six_no'])

        elif query_type == '4':
            frame_no = self.cleaned_data.get('frame_no', '')
            if not frame_no:
                raise forms.ValidationError(
                    self.err_msg['no_frame_no'])
            elif not re.match(r'^[0-9A-Z]{17}$', frame_no):
                raise forms.ValidationError(
                    self.err_msg['wrong_frame_no'])

        return self.cleaned_data
