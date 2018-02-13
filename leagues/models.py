# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class League(models.Model):
    name = models.CharField(max_length=200)
    owner = models.OneToOneField(User)
    participants = models.ManyToManyField(User, related_name='participants')
    created_date = models.DateTimeField('date created')
    signup_code = models.CharField(max_length=15, unique=True, blank=False)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name