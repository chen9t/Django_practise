#encoding=utf-8
import requests
from django.template import RequestContext
from django.shortcuts import render_to_response
from vehicle_violation_query.models import City, CarInfo, ViolationRecord
from django.core.exceptions  import ObjectDoesNotExist
from requests.exceptions import Timeout

def query(request):

    if request.method == 'POST':
        #获取查询参数
        provincename = request.POST.get('province', '')
        cityname = request.POST.get('cityname', '')
        hphm = request.POST.get('license_plate_num', '')
        engineno = request.POST.get('engine_no', '')
        city = City.objects.exclude(id=0).get(name=cityname)
        #写入参数
        payload = {'city': city.pinyin, 'hphm': hphm, 'hpzl': '02', 'engineno': engineno, 'cityname': cityname, 'provincename': provincename, 'format': 'json'}
        #获得记录信息
        r = requests.get("http://api.open.baidu.com/pae/traffic/api/query", params=payload)

        if r.json()['vehicle_status'] == 'ok':
            #车辆信息无误
            record_list = r.json()['data']['lists']
            #将记录按照日期进行排序
            record_list.sort(key=lambda obj:obj.get('date'), reverse=True)
            #待插入的记录
            need_to_insert = []

            try:
                #获得汽车相关信息
                car_info = CarInfo.objects.get(license_plate_num=hphm)
            except ObjectDoesNotExist:
                #如果还没有这辆车的记录
                car_info = CarInfo(license_plate_num=hphm, engine_no=engineno)
                car_info.save()
                need_to_insert = record_list

            #已有记录,找到新增加的记录
            old_record = ViolationRecord.objects.filter(car_info=car_info).order_by('-date')

            if not old_record:
                need_to_insert = record_list
            else:
                latest = old_record[0].date
                for record in record_list:
                    if record['date'] <= latest:
                        break
                    need_to_insert.append(record)       

            #将新记录存进数据库
            for new_record in need_to_insert:
                violation_record = ViolationRecord(car_info=car_info, area=new_record['area'], money=new_record['money'],
                    chuli=new_record['chuli'], fen=new_record['fen'], date=new_record['date'], act=new_record['act'])
                violation_record.save()

            return render_to_response('query.html', {'record_list': record_list}, context_instance=RequestContext(request))

        else:
            #输入车辆信息有误
            return render_to_response('query.html', {'error_msg': '您输入的信息有误，请校验后重新查询！'}, context_instance=RequestContext(request))
    else:
        return render_to_response('query.html', context_instance=RequestContext(request))

def send_request(request, payload):

    try:
        r = requests.get("http://api.open.baidu.com/pae/traffic/api/query", params=payload, timeout=10)
    except Timeout:
        return render_to_response('query.html', {'error_msg': '请求超时，请重新查询！'}, context_instance=RequestContext(request))

    if r.status_code == 200:
        return r
    else:
       return render_to_response('query.html', {'error_msg': '请求错误，请重新查询！'}, context_instance=RequestContext(request)) 