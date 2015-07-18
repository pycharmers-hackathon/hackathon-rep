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
from random import random
from model import PatrolStation


@csrf_exempt
def index(request, page=None):
    coordinates = []
    with io.open('c:/users/theo/desktop/coordinates.txt', 'r') as csv_file:
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
        PatrolStation.objects.filter(id=counter + 1).update(latitude=float(coordinates[i][0]),
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
