# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-01-25 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CloudRoni', '0012_team_team_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='point',
            name='team',
            field=models.TextField(default='default', max_length=200),
            preserve_default=False,
        ),
    ]
