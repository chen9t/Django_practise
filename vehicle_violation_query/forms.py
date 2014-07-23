#encoding=utf-8
import re
from django import forms


class CarInfoForm(forms.Form):

    province = forms.CharField(max_length=10, error_messages={'required': '请选择省份'})
    cityname = forms.CharField(max_length=10, error_messages={'required': '请选择城市'})
    car_province = forms.CharField(max_length=1, error_messages={'required': '请输入车牌号码'})
    license_plate_num = forms.CharField(max_length=6, error_messages={'required': '请输入车牌号码'})
    engine_no = forms.CharField(max_length=6, error_messages={'required': '请输入发动机号后6位'})

    def clean_license_plate_num(self):
        license_plate_num = self.cleaned_data['license_plate_num']
        if not re.search(r'^([0-9A-Z]{6})$', license_plate_num):
            raise forms.ValidationError('请输入正确的车牌号码')
        return license_plate_num

    def clean_engine_no(self):
        engine_no = self.cleaned_data['engine_no']
        if len(engine_no) != 6:
            raise forms.ValidationError('请输入正确的发动机号后6位')
        return engine_no
