# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-25 17:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CloudRoni', '0011_auto_20180125_0156'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team_points',
            field=models.IntegerField(default=0),
        ),
    ]
