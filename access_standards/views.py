# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from access_standards.models import AccessStandard
from django.utils import simplejson
from django.views.generic import TemplateView, ListView


class AboutView(TemplateView):

    http_method_names = ['get', ]
    template_name = 'about.html'


class CityView(ListView):

    template_name = 'standard_list.html'
    context_object_name = 'standard_list'
    queryset = AccessStandard.objects.all()


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
