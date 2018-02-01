# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import pdb
import mock

from django.utils import timezone
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from users.models import PhoneNumber
from users.forms import PhoneNumberForm
from users.views import format_twilio_number

# Create your tests here.
class UserViewsTests(TestCase):

    def setUp(self):
        user = User.objects.create(username='jab')
        user.set_password('1234')
        user.email = 'test_email@gmail.com'
        user.save()
        self.new_user = user

    def login_user(self):
        self.client.login(username='jab',password='1234')

    def test_update_account(self):
        self.login_user()
        response = self.client.get('/users/' + str(self.new_user.id) + '/account/')

        self.assertTrue(self.new_user.username in response.content)

    def test_update_account_user_is_correct(self):
        user_two = User.objects.create(username='meow')
        user_two.set_password('1234')
        user_two.save()
        self.login_user()
        response = self.client.get('/users/' + str(self.new_user.id + 1) + '/account/')

        self.assertEqual(response.status_code, 403)

    def test_phone_number_page_loads(self):
        self.login_user()
        response = self.client.get('/users/update_phone_number/')

        self.assertTrue("Number:" in response.content)

    @mock.patch('users.models.PhoneNumber.is_valid_number', return_value=True)
    def test_create_phone_number(self, is_valid_number_mock):
        self.login_user()
        number_count = PhoneNumber.objects.count()
        response = self.client.post('/users/update_phone_number/', {'number': '7143378530'})

        self.assertEqual(is_valid_number_mock.call_count, 1)
        self.assertEqual(PhoneNumber.objects.count(), number_count + 1)

    @mock.patch('users.models.PhoneNumber.is_valid_number', return_value=True)
    def test_update_phone_number(self, is_valid_number_mock):
        self.login_user()
        number = PhoneNumber(user = self.new_user,
                                twilio_formatted_number = "+17143378530",
                                number = "7143378530",
                                created_date = timezone.now(),
                                is_valid_phone_number = True)
        number.save()
        response = self.client.post('/users/update_phone_number/', {'number': '3234008000'})

        self.assertEqual(is_valid_number_mock.call_count, 1)
        self.assertEqual(PhoneNumber.objects.last().number, '3234008000')

    def test_twilio_formatting(self):
        formatted_number = format_twilio_number("7143378530")

        self.assertEqual("+17143378530", formatted_number)