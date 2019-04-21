from django.contrib.auth.models import User
from django.test import TestCase
from login.forms import LoginForm

class TestUserForm(TestCase):

    def test_TC_Login_001(self):
        # test valid data ==> data field is not blank
        vaild_data = {
            "username": "testuser2",
            "password": "Password123"
        }
        form = LoginForm(data = vaild_data)
        self.assertTrue(form.is_valid(), "All field entered")

    def test_TC_Login_001_fail1(self):
        # test for invalid field input, username left blank case
        invalid_data = {
            "username": None,
            "password": "Password123"
        }
        form = LoginForm(data = invalid_data)
        self.assertFalse(form.is_valid(), "Username field is empty")
        self.assertEqual(form.errors['username'], ["This field is required."])

    def test_TC_Login_001_fail2(self):
        # test for invalid field input, password left blank case
        invalid_data = {
            "username": "testuser2",
            "password": None
        }
        form = LoginForm(data=invalid_data)
        self.assertFalse(form.is_valid(), "Password field is empty")
        self.assertEqual(form.errors['password'], ["This field is required."])

    def test_TC_Login_001_fail3(self):
        # test for invalid field input, password and username left blank case
        invalid_data = {
            "username": None,
            "password": None
        }
        form = LoginForm(data=invalid_data)
        self.assertFalse(form.is_valid(), "Username and Password field is empty")
        self.assertEqual(form.errors['username'], ["This field is required."])