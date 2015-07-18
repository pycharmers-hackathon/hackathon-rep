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
from random import random


@csrf_exempt
def index(request, page=None):
    coordinates = []
    with io.open('coordinates.txt', 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            for row in reader:
                coordinates.append((row[0], row[1]))
    counter = 2928
    for i in range(1375):
        unlead95 = 1 + random()
        unlead100 = 1 + random()
        super_unlead = 1 + random()
        gas = 1 + random()
        dieser = 1 + random()
        t = float(coordinates[i][0])
        PatrolStation.objects.filter(id=counter + 1).update(latitude=t,
                                                            longitude=float(coordinates[i][1]),
                                                            unleaded95=unlead95,
                                                            unleaded100=unlead100,
                                                            super_unleaded=super_unlead,
                                                            gas=gas,
                                                            diesel=dieser)
    return render(request, 'index.html')

def nearest_patrol_stations(request):
    latitute = request.get('lat')
    longitute = request.get('lng')

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