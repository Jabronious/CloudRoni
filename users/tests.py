# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

import pdb

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