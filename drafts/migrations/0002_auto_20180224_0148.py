# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-24 01:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drafts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='draft',
            name='current_team',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='CloudRoni.Team'),
        ),
    ]
