# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from access_standards.models import AccessStandard
from django.utils import simplejson


def index(request):

    if request.method == 'GET' and 'city' in request.GET:
        city = request.GET['city']
        s = get_object_or_404(AccessStandard, city=city)
        standard = {'city': city, 'emission_standard': s.emission_standard,
                            'standard_details': s.standard_details,
                            'DVM': s.DVM}
        return HttpResponse(simplejson.dumps(standard, ensure_ascii=False)) 
    else:
        return render_to_response('index.html')


def standard(request):

    if request.method == 'GET' and 'standard' in request.GET:

        standard = request.GET['standard']
        s = AccessStandard.objects.filter(emission_standard=standard)
        print type(s)
        return render_to_response('search.html', {'city_list': s})
    else:
        return render_to_response('search.html')
