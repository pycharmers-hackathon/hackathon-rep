from __future__ import unicode_literals
from django.db import models


class PatrolStation(models.Model):
    owner = models.CharField()
    region = models.CharField()
    address = models.CharField()
    type = models.CharField()
    phone = models.CharField()
    city = models.CharField()
    post_code = models.CharField()
    prefecture = models.CharField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    unleaded95 = models.FloatField()
    unleaded100 = models.FloatField()
    super_unleaded = models.FloatField()
    gas = models.FloatField()
    diesel = models.FloatField()

