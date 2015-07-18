from django.db import models

# Create your models here.


class PatrolStation(models.Model):
    owner = models.CharField(max_length=150)
    region = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    type = models.CharField(max_length=150)
    phone = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    post_code = models.CharField(max_length=150)
    prefecture = models.CharField(max_length=150)
    latitude = models.FloatField()
    longitude = models.FloatField()
    unleaded95 = models.FloatField()
    unleaded100 = models.FloatField()
    super_unleaded = models.FloatField()
    gas = models.FloatField()
    diesel = models.FloatField()
