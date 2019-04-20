from django.contrib.auth.models import User
from django.http import request
from django.test import TestCase, Client;
from createuser.forms import UserForm;


class SetupClass(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="JamesLee", password='FlowerChild12', email='test@test.com')


class UserForm(TestCase):
    def test_UserForm_valid(self):
        valid_data = {'Username':'Sally100', 'Password':'password123', 'Email':'test@test.com'}
        form = UserForm(data = valid_data)
        self.assertTrue(form.is_valid())

    def test_UserForm_invalid(self):
        invalid_data = {'username':'', 'password':'password123', 'email':'test@test.com'}
        form = UserForm(invalid_data)
        self.assertFalse(form.is_valid())

