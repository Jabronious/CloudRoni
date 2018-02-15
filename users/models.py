# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings
from leagues.models import League
import pdb

# Create your models here.
class PhoneNumber(models.Model):
    user = models.OneToOneField(User)
    twilio_formatted_number = models.CharField(max_length=12)
    number = models.CharField(max_length=10)
    created_date = models.DateTimeField('date published')
    is_valid_phone_number = models.BooleanField(default=True)

    def __str__(self):
        return self.number

    def is_valid_number(self):
        try:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            response = client.lookups.phone_numbers(self.number).fetch(type="carrier", country_code="US")
            return True
        except TwilioRestException as e:
            return False