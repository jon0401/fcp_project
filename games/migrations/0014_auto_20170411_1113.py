# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-11 03:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0013_auto_20170411_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='release_datetime',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]