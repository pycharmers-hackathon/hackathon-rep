# coding=utf-8

from django.http import *
from django.shortcuts import render_to_response
from django.template import Template, Context
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core import serializers
from django.core.context_processors import csrf
from django.shortcuts import render

import csv
import io, sys
from data.models import PatrolStation


@csrf_exempt
def index(request, page=None):
    t = get_template('smartfuel.html')
    fuel_list = ['unleaded95', 'unleaded100', 'diesel', 'gas']
    html = []
    for i in range(1, 5):
        html.append(saggest_html(request, (2928 + i), fuel_list[i - 1]))

    html1 = t.render(Context({'html1': html[0],
                             'html2': html[1],
                             'html3': html[2],
                             'html4': html[3]}))
    return HttpResponse(html1)


def nearest_fuel_stations(request):
    data = serializers.serialize('json', PatrolStation.objects.order_by('unleaded95'),
                                 fields=('owner', 'latitude', 'longitude',
                                 'address', 'unleaded95'))
    return HttpResponse(data, content_type='application/json')

def aco_controller(request):
    source = (37.979946, 23.727801)
    target = (40.851363, 25.875331)
    capacity = 20
    initial_quanity = 10
    consumption = 0.1
    fuel = 'unleaded95'
    overall_dist = 1500
    a = aco(PatrolStation.objects.values(), fuel, capacity, initial_quanity,
        overall_dist, consumption, source, target)
    return HttpResponse('fsfs', content_type='plain/text')

@csrf_exempt
def insert_data(request, page=None):
    with io.open('PratiriaPouApostellounStoixeiaGGPS.csv', 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            counter = 0
            flag = True
            for row in reader:
                if (flag):
                    flag = False
                row = [x for x in row]
                r = PatrolStation.objects.create(owner = str(row[0]),
                                                     region = row[1],
                                                     address = row[2],
                                                     type = row[3],
                                                     phone = row[4],
                                                     city = row[5],
                                                     post_code = row[6],
                                                     prefecture = row[7],
                                                     latitude = 0.0,
                                                     longitude = 0.0,
                                                     unleaded95 = 0.0,
                                                     unleaded100 = 0.0,
                                                     super_unleaded = 0.0,
                                                     gas = 0.0,
                                                     diesel = 0.0)
                r.save()

@csrf_exempt
def saggest_html(request, id, type):
    t = get_template('suggest.html')
    color_list = ['bg-aqua', 'bg-green', 'bg-yellow', 'bg-red']
    object = PatrolStation.objects.get(id = id)
    if (type == 'unleaded95'):
        color = color_list[0]
        price = object.unleaded95
    elif (type == 'unleaded100'):
        color = color_list[1]
        price = object.unleaded100
    elif (type == 'diesel'):
        color = color_list[2]
        price = object.diesel
    else:
        color = color_list[3]
        price = object.gas

    html = t.render(Context({'color1': color,
                             'price': price,
                             'address': object.address,
                             'fuel': type}))

    return html;