#encoding=utf-8
import requests
from requests.exceptions import Timeout, HTTPError

from django.views.generic import FormView
from django.core.exceptions  import ObjectDoesNotExist

from vehicle_violation_query.models import City, CarInfo, ViolationRecord
from vehicle_violation_query.forms import CarInfoForm

from ajaxres import AjaxResponseMixin

from vehicle_violation_query.query_settings import REQUEST_URL, TIME_OUT


class ViolationQuery(FormView, AjaxResponseMixin):
    
    template_name='query.html'
    http_method_names = ['get', 'post']
    form_class = CarInfoForm
    err_msg = {
        'no_record': u'恭喜您，没有违章记录！',
        'wrong_message': u'您输入的信息有误，请校验后重新查询！',
        'time_out': u'请求超时，请重新查询！',
        'request_failure': u'请求失败，请重新查询！',
    }


    def form_valid(self, form):
        context = {}
        # 获取查询参数
        provincename = form.cleaned_data['province']
        cityname = form.cleaned_data['cityname']
        car_province = form.cleaned_data['car_province']
        license_plate_num= form.cleaned_data['license_plate_num']
        engineno = form.cleaned_data['engine_no']
        hphm = ''.join([car_province, license_plate_num])
        city = City.objects.exclude(parent=0).get(name=cityname)
        # 写入参数
        payload = {'city': city.pinyin, 'hphm': hphm, 'hpzl': '02', 'engineno': engineno, 
                    'cityname': cityname, 'provincename': provincename, 'format': 'json'}
        
        try:  # 发送请求
            r = self.send_request(payload)
            if r.json()['vehicle_status'] == 'ok':  # 车辆信息无误
                record_list = []
                if 'lists' not in r.json()['data']:  # 没有违章记录
                    context = {'count': 0}
                else:  # 有违章记录
                    data = {}
                    record_list = r.json()['data']['lists']
                    # 将记录按照日期进行排序
                    record_list.sort(
                        key=lambda obj: obj.get('date'), reverse=True)
                    # 返回违章信息
                    data['record_list'] = record_list
                    data['point'] = r.json()['data']['score']
                    data['forfeit'] = r.json()['data']['forfeit']
                    count = r.json()['data']['count']
                    context = {'count': count, 'data': data}

                #将数据存入数据库（包括未录入的车和违章信息）
                self.store_record(hphm, engineno, record_list)
            else:  # 输入车辆信息有误
                self.update_errors(self.err_msg['wrong_message'])

        except Timeout:  # 请求超时
            self.update_errors(self.err_msg['time_out'])
        except HTTPError:  # 请求失败
            self.update_errors(self.err_msg['request_failure'])

        return self.ajax_response(context)

    def send_request(self, payload):
        '''发送请求'''
        try:
            r = requests.get(REQUEST_URL, params=payload, timeout=TIME_OUT)
        except Timeout:
            raise Timeout

        if r.status_code == 200:
            return r
        else:
            r.raise_for_status() 
            

    def store_record(self, hphm, engineno, record_list):
        '''将数据存入数据库'''
        # 待插入的记录
        need_to_insert = []
        try:
            # 获得汽车相关信息
            car_info = CarInfo.objects.get(license_plate_num=hphm)
            # 已有记录,找到新增加的记录
            old_record = ViolationRecord.objects.filter(car_info=car_info).order_by('-date')

            if not old_record:
                need_to_insert = record_list
            else:
                latest = old_record[0].date
                for record in record_list:
                    if record['date'] <= latest:
                        break
                    need_to_insert.append(record)

        except ObjectDoesNotExist: # 如果还没有这辆车的记录
            car_info = CarInfo(license_plate_num=hphm, engine_no=engineno)
            car_info.save()
            need_to_insert = record_list

        # 将新记录添加到插入列表中
        insert_list = []
        for new_record in need_to_insert:
            violation_record = ViolationRecord(car_info=car_info, area=new_record['area'], money=new_record['money'],
                chuli=new_record['chuli'], fen=new_record['fen'], date=new_record['date'], act=new_record['act'])
            insert_list.append(violation_record)
        # 批量插入
        ViolationRecord.objects.bulk_create(insert_list)
