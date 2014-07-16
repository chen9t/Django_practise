#encoding=utf-8
import requests
from django.template import RequestContext
from django.shortcuts import render_to_response

def query(request):

    if request.method == 'POST':
        provincename = request.POST.get('province', '')
        cityname = request.POST.get('cityname', '')
        hphm = request.POST.get('license_plate_num', '')
        engineno = request.POST.get('engine_no', '')

        payload = {'city': 'nanjing', 'hphm': hphm, 'hpzl': '02', 'engineno': engineno, 'cityname': cityname, 'provincename': provincename, 'format': 'json'}

        r = requests.get("http://api.open.baidu.com/pae/traffic/api/query", params=payload)
        record_list = r.json()['data']['lists']

        return render_to_response('query.html', {'record_list': record_list}, context_instance=RequestContext(request))
    else:
        return render_to_response('query.html', context_instance=RequestContext(request))
