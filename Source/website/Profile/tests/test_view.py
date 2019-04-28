import datetime
from ticket_creation.models import All_Tickets
from django.test import TestCase
from django.contrib.auth.models import User
from ticket_creation.models import Ticket
from django.urls import reverse
from django.test import Client
from createuser.models import Extended_User
from Profile.models import Profile


class ProfileTestView(TestCase):
    @classmethod
    def setUp(self):
        self.client = Client()
        test_user2_profile = Profile.objects.create(username='testuser2',
                                                    phoneNumber='12345679',
                                                    email='testing@test.com',
                                                    user='testuser2')

        test_user2 = Extended_User.objects.create(username='testuser2',
                                                  password='HelloSekai123',
                                                  email='testing@test.com',
                                                  phoneNumber='12345679',
                                                  notify_email=True,
                                                  notify_sms=False)
        test_user2.set_password('HelloSekai123')
        test_user2.save()
        test_user2.is_active = True

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('Profile:viewProfile'))
        self.assertRedirects(response,'/')

    def test_Profile_viewProfile_status_code(self):
        response = self.client.get(reverse('Profile:viewProfile'))
        self.assertEquals(response.status_code, 302)

    def test_valid_edit_username_Profile(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        # print(login)
        response = self.client.post(reverse('Profile:viewProfile'), {
            'username': 'TestUser2',
            'password': 'HelloSekai123',
            'email': 'testing@test.com',
            'phoneNumber': '12345679',
            'notify_email': True,
            'notify_sms': False,
        })
        # print(response)
        # print(response.context['error_message'])
        self.assertEqual(response.context['error_message'], 'Edit profile success')


    def test_invalid_username_Profile(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        # print(login)
        response = self.client.post(reverse('Profile:viewProfile'),{
            'username': 'test@user2',
            'password': 'HelloSekai123',
            'email': 'testing@test.com',
            'phoneNumber': '12345679',
            'notify_email':  True,
            'notify_sms': False,
        })
        # print(response)
        # print(response.context['error_message'])
        self.assertEqual(response.context['error_message'],'Please ensure input fields are valid')

    def test_valid_edit_Email_Profile(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        # print(login)
        response = self.client.post(reverse('Profile:viewProfile'), {
            'username': 'testuser2',
            'password': 'HelloSekai123',
            'email': 'testing@test.com',
            'phoneNumber': '12345679',
            'notify_email': True,
            'notify_sms': False,
        })
        # print(response)
        # print(response.context['error_message'])
        self.assertEqual(response.context['error_message'], 'Edit profile success')

    def test_valid_edit_SMS_Profile(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        # print(login)
        response = self.client.post(reverse('Profile:viewProfile'), {
            'username': 'testuser2',
            'password': 'HelloSekai123',
            'email': 'testing@test.com',
            'phoneNumber': '12345679',
            'notify_email': False,
            'notify_sms': True,
        })
        # print(response)
        # print(response.context['error_message'])
        self.assertEqual(response.context['error_message'], 'Edit profile success')


    def test_empty_password_Profile(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        # print(login)
        response = self.client.post(reverse('Profile:viewProfile'), {
            'username': 'testuser2',
            'password': None,
            'email': 'testing@test.com',
            'phoneNumber': '12345679',
            'notify_email': True,
            'notify_sms': False,
        })
        # print(response)
        # print(response.context['error_message'])
        self.assertEqual(response.context['error_message'], 'Edit profile success')

    def test_invalid_email_Profile(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        # print(login)
        response = self.client.post(reverse('Profile:viewProfile'),{
            'username': 'test@user2',
            'password': 'HelloSekai123',
            'email': 'testing@@test.com',
            'phoneNumber': '12345679',
            'notify_email':  True,
            'notify_sms': False,
        })
        # print(response)
        # print(response.context['error_message'])
        self.assertEqual(response.context['error_message'],'Please ensure input fields are valid')

    def test_invalid_phoneNumber_Profile(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        # print(login)
        response = self.client.post(reverse('Profile:viewProfile'),{
            'username': 'test@user2',
            'password': 'HelloSekai123',
            'email': 'testing@test.com',
            'phoneNumber': '1234567e',
            'notify_email':  True,
            'notify_sms': False,
        })
        # print(response)
        # print(response.context['error_message'])
        self.assertEqual(response.context['error_message'],'Please ensure input fields are valid')

    def test_invalid_notify_All_False_Profile(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        # print(login)
        response = self.client.post(reverse('Profile:viewProfile'),{
            'username': 'test@user2',
            'password': 'HelloSekai123',
            'email': 'testing@test.com',
            'phoneNumber': '12345679',
            'notify_email':  False,
            'notify_sms': False,
        })
        # print(response)
        # print(response.context['error_message'])
        self.assertEqual(response.context['error_message'],
                         "Please ensure input fields are valid")

    def test_viewProfile(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        response = self.client.get(reverse('Profile:viewProfile'))
        # print(response.context['user_information'])
        self.assertEqual(response.context['user_information'],
                         {'username': 'testuser2',
                          'email': 'testing@test.com',
                          'phoneNumber': '12345679',
                          'notify_email': True,
                          'notify_sms': False})
