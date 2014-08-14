# -*- coding: utf-8 -*-
import re

from django import forms


class InsuranceQueryForm(forms.Form):

    QUERY_TYPE_CHOICES = (('by_policeno', '根据保单号查询'),
                                            ('by_licenseno_VIN', '根据车牌号和车架号后六位查询'),
                                            ('by_VIN_engineno', '根据车架号后六位和发动机号后六位查询'),
                                            ('by_VIN', '根据车架号查询'))

    err_msg = {
        'no_policy_no': u'请输入保单号',
        'no_license_no': u'请输入车牌号',
        'no_VIN_last_six': u'请输入车架号后6位',
        'no_engine_last_six_no': u'请输入发动机号后6位',
        'no_VIN': u'请输入车架号',
        'wrong_policy_no': u'请输入正确的保单号',
        'wrong_license_no': u'请输入正确的车牌号',
        'wrong_VIN_last_six': u'请输入正确的车架号后6位',
        'wrong_VIN': u'请输入正确的车架号'
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

    VIN_last_six = forms.CharField(
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

    VIN = forms.CharField(
        min_length=17,
        max_length=17,
        required=False,
        error_messages={
            'min_length': u'车架号过短',
            'max_length': u'车架号过短'
        })

    def clean(self):
        query_type = self.cleaned_data.get('query_type', '')

        if query_type == 'by_policeno':
            policy_no = self.cleaned_data.get('policy_no', '')
            if not policy_no:
                raise forms.ValidationError(
                    self.err_msg['no_policy_no'])
            elif not re.match(r'^[0-9A-Z]{22}$', policy_no):
                raise forms.ValidationError(
                    self.err_msg['wrong_policy_no'])

        elif query_type == 'by_licenseno_VIN':
            license_no = self.cleaned_data.get('license_no', '')
            if not license_no:
                raise forms.ValidationError(
                    self.err_msg['no_license_no'])
            elif not re.match(ur'^苏[A-Z][A-Z0-9]{5}$', license_no):
                raise forms.ValidationError(
                    self.err_msg['wrong_license_no'])

            VIN_last_six = self.cleaned_data.get('VIN_last_six', '')
            if not VIN_last_six:
                raise forms.ValidationError(
                    self.err_msg['no_VIN_last_six'])
            elif not re.match(r'^[0-9A-Z]{6}$', VIN_last_six):
                raise forms.ValidationError(
                    self.err_msg['wrong_VIN_last_six'])

        elif query_type == 'by_VIN_engineno':
            VIN_last_six = self.cleaned_data.get('VIN_last_six', '')
            if not VIN_last_six:
                raise forms.ValidationError(
                    self.err_msg['no_VIN_last_six'])
            elif not re.match(r'^[0-9A-Z]{6}$', VIN_last_six):
                raise forms.ValidationError(
                    self.err_msg['wrong_VIN_last_six'])

            engine_last_six_no = self.cleaned_data.get('engine_last_six_no', '')
            if not engine_last_six_no:
                raise forms.ValidationError(
                    self.err_msg['no_engine_last_six_no'])

        elif query_type == 'by_VIN':
            VIN = self.cleaned_data.get('VIN', '')
            if not VIN:
                raise forms.ValidationError(
                    self.err_msg['no_VIN'])
            elif not re.match(r'^[0-9A-Z]{17}$', VIN):
                raise forms.ValidationError(
                    self.err_msg['wrong_VIN'])

        return self.cleaned_data
