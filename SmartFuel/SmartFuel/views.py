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
from model import PatrolStation
reload(sys)
sys.setdefaultencoding('utf-8')


@csrf_exempt
def index(request, page=None):
    with io.open('c:/users/theo/desktop/PratiriaPouApostellounStoixeiaGGPS.csv', 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            counter = 0
            for row in reader:
                row = [x.decode('utf-8') for x in row]
            r = PatrolStation(row[0], row[1], row[2], row[3], row[4], row[5],
                              row[6], row[7], 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            r.save()
    return render(request, 'index.html')

def nearest_patrol_stations(request):
    latitute = request.get('lat')
    longitute = request.get('lng')
