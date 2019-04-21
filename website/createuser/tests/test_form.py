from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import TestCase
from createuser.forms import UserForm

# run in Source\website --> python manage.py test createuser.tests.test_form.TestUserForm


class TestUserForm(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='JaneLee',
                                             password='password123',
                                             email='test@test.com',
                                             phoneNumber='12345678',
                                             notify_email=True,
                                             notify_sms=False
                                             )

    def test_C_AC_Create_001(self):
        # test valid data
        valid_data = {
            "username": "Johnlee",
            "password": "password",
            "email": "test@test.com",
            "phoneNumber": "98765432",
            "notify_email": True,
            "notify_sms": False
        }

        form = UserForm(data= valid_data)
        self.assertTrue(form.is_valid(), 'Form is valid')

    def test_TC_AC_Create_003_bt1(self):
        # boundary cases for invalid email: extra char
        invalid_data = {
            "username": "Johnlee",
            "password": "password",
            "email": "test@@test.com",
            "phoneNumber": "98765432",
            "notify_email": True,
            "notify_sms": False
        }
        form = UserForm(data = invalid_data)
        self.assertFalse(form.is_valid(), 'Email format is wrong')

    def test_TC_AC_Create_003_bt2(self):
        # boundary cases for invalid email: illegal chars
        invalid_data = {
            "username": "Johnlee",
            "password": "password",
            "email": "test*test@test.com",
            "phoneNumber": "98765432",
            "notify_email": True,
            "notify_sms": False,
        }
        form = UserForm(data = invalid_data)
        self.assertFalse(form.is_valid(), 'Email format is wrong, illegal char')


    def test_TC_AC_Create_003_bt3(self):
        # boundary cases for invalid email: missing input
        invalid_data = {
            "username": "Johnlee",
            "password": "password",
            "email": None,
            "phoneNumber": "98765432",
            "notify_email": True,
            "notify_sms": False,
        }
        form = UserForm(data = invalid_data)
        self.assertFalse(form.is_valid(), 'No Email')

    def test_TC_AC_Create_003_bt4(self):
        # boundary cases for invalid email: email is too long
        invalid_data = {
            "username": "Johnlee",
            "password": "password",
            "email": "testtesttesttesttesttesttesttesttesttesttest@test.com",
            "phoneNumber": "98765432",
            "notify_email": True,
            "notify_sms": False,
        }
        form = UserForm(data = invalid_data)
        self.assertFalse(form.is_valid(), 'No Email')

    def test_TC_AC_Create_006_bt1(self):
        # boundary case for invalid username: username not filled
        invalid_data = {
            "username": None,
            "password": "password",
            "email": "test@test.com",
            "phoneNumber": "98765432",
            "notify_email": True,
            "notify_sms": False,
        }
        form = UserForm(data = invalid_data)
        self.assertFalse(form.is_valid(), 'No username input')

    def test_TC_AC_Create_006_bt2(self):
        # boundary case for invalid username: username is too short <5 letters
        invalid_data = {
            "username": "j",
            "password": "password",
            "email": "test@test.com",
            "phoneNumber": "98765432",
            "notify_email": True,
            "notify_sms": False,
        }
        form = UserForm(data=invalid_data)
        self.assertFalse(form.is_valid(), 'Username is too short')

    def test_TC_AC_Create_006_bt3(self):
        # boundary case for invalid username: username is too long > 30 chars
        invalid_data = {
            "username": "helloworlditisanamazingdaytodayladida",
            "password": "password",
            "email": "test@test.com",
            "phoneNumber": "98765432",
            "notify_email": True,
            "notify_sms": False,
        }
        form = UserForm(data=invalid_data)
        self.assertFalse(form.is_valid(), 'Username is too long')

    def test_TC_AC_Create_006_bt4(self):
        # boundary case for invalid username: contains illegal characters
        invalid_data = {
            "username": "jane**lee",
            "password": "password",
            "email": "test@test.com",
            "phoneNumber": "98765432",
            "notify_email": True,
            "notify_sms": False,
        }
        form = UserForm(data=invalid_data)
        self.assertFalse(form.is_valid(), 'illegl characters in username')

    def test_TC_AC_Create_006_bt5(self):
        # boundary case for invalid username: username already taken
        # how to write test case for this?
        pass;

    def test_TC_AC_Create_007_bt1(self):
        # invalid password: length too short, min 5 chars
        invalid_data = {
            "username": "JaneLee",
            "password": "Pas1",
            "email": "test@test.com"
        }
        form = UserForm(data=invalid_data)
        self.assertFalse(form.is_valid(), 'password too short')

    def test_TC_AC_Create_007_bt2(self):
        # invalid password: length too long, max 20 chars
        invalid_data = {
            "username": "JaneLee",
            "password": "Pas1hjhjhjhjhjjhjhjhjhjhjhjhjhjhjhjhjhjhj",
            "email": "test@test.com"
        }
        form = UserForm(data=invalid_data)
        self.assertFalse(form.is_valid(), 'password too long')

    def test_TC_AC_Create_007_bt3(self):
        # invalid password: all small letters
        invalid_data = {
            "username": "JaneLee",
            "password": "password",
            "email": "test@test.com"
        }
        form = UserForm(data=invalid_data)
        self.assertFalse(form.is_valid(), "need to have Capital letters and Numbers")

    def test_TC_AC_Create_007_bt4(self):
        # invalid password: length too short, min 5 chars
        invalid_data = {
            "username": "JaneLee",
            "password": "Password12&^7",
            "email": "test@test.com"
        }
        form = UserForm(data=invalid_data)
        self.assertFalse(form.is_valid(), 'Password has illegal characters')