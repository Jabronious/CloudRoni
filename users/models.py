# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PhoneNumber(models.Model):
    user = models.ForeignKey(User)
    twilio_formatted_number = models.CharField(max_length=12)
    number = models.CharField(max_length=10)
    created_date = models.DateTimeField('date published')

    def __str__(self):
        return self.number

    def validate_number(self):
        #put validation logic
        return

    def format_twilio_number(self):
        return '+1' + self.number