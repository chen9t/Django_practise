from django.conf import settings

REQUEST_URL = getattr(settings, 'REQUEST_URL', "http://api.open.baidu.com/pae/traffic/api/query")
TIME_OUT = getattr(settings, 'TIME_OUT', 10)
