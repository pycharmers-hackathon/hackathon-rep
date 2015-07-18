from django.http import *
from django.shortcuts import render_to_response
from django.template import Template, Context
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core import serializers
from django.core.context_processors import csrf
from django.shortcuts import render
from data.models import *

@csrf_exempt
def index(request, page=None):
    return render(request, 'index.html')