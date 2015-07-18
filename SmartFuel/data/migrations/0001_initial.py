# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PatrolStation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('owner', models.CharField(max_length=150)),
                ('region', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=150)),
                ('type', models.CharField(max_length=150)),
                ('phone', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=150)),
                ('post_code', models.CharField(max_length=150)),
                ('prefecture', models.CharField(max_length=150)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('unleaded95', models.FloatField()),
                ('unleaded100', models.FloatField()),
                ('super_unleaded', models.FloatField()),
                ('gas', models.FloatField()),
                ('diesel', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
