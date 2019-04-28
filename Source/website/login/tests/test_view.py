from django.contrib.auth.models import User
from createuser.models import Extended_User
from django.test import TestCase
from django.urls import reverse
from django.test import Client

from login.views import error_message_incorrect_userpass, error_message_empty_input, error_message_invalid_input


class LoginInstanceViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create an existing User
        test_user1 = Extended_User.objects.create(username='testuser1')
        test_user1.set_password('HelloWorld123')
        test_user1.save()
        test_user2 = Extended_User.objects.create(username='testuser2',
                                                  password='HelloSekai123',
                                                  email='testing2@test.com',
                                                  phoneNumber='12345679',
                                                  notify_email=True,
                                                  notify_sms=False)
        test_user2.set_password('HelloSekai123')
        # test_user2.is_active = True
        test_user2.save()

    # Test for correct template being used
    def test_uses_correct_template(self):
        response = self.client.get(reverse('login:index'))
        self.assertTemplateUsed(response, 'login.html')

    # Test for Get Request, should return an empty Login form
    def test_login_page(self):
        response = self.client.get(reverse('login:index'))
        self.assertEqual(response.status_code, 200)

    # Test for Post Request
    def test_valid_login(self):
        # sucessful login and redirected to home page
        response = self.client.post(reverse("login:index"), {'username': 'testuser1',
                                                             'password': 'HelloWorld123'})
        self.assertRedirects(response,reverse("home:index"))
        # response = self.client.get(reverse("home:index"))
        self.assertEqual(response.status_code, 302)

    def test_invalid_login_username(self):
        # upon entering invalid details, user is not redirected
        response = self.client.post(reverse("login:index"), {'username': 'testuser3',
                                                             'password': 'HelloWorld123'})

        # in context object -> act like a dictionary with 'error_message" as a key
        self.assertTrue('error_message' in response.context)
        # Check that the right Error Message is displayed
        self.assertEqual(response.context['error_message'], error_message_incorrect_userpass)

    def test_invalid_login_password(self):
        # invalid password
        response = self.client.post(reverse("login:index"), {'username': 'testuser1',
                                                             'password': 'HelloWorld1234'})

        self.assertTrue('error_message' in response.context)
        self.assertEqual(response.context['error_message'], error_message_incorrect_userpass)

    def test_invalid_login_all_empty(self): # this may be covered by testing of Forms
        # upon entering invalid details, user is not redirected
        response = self.client.post(reverse("login:index"), {'username': None,
                                                             'password': None})

        # in context object -> act like a dictionary with 'error_message" as a key
        self.assertTrue('error_message' in response.context)
        # Check that the right Error Message is displayed
        self.assertEqual(response.context['error_message'], error_message_incorrect_userpass)

    # def test_valid_logout(self):
    #     # Log user in
    #     user_login  = self.client.login(username = 'testuser1', password = 'HelloWorld123')
    #     # Check response Code
    #     response = self.client.get(reverse("home:index"))
    #     self.assertEqual(response.status_code, 200)
    #     # Log User out
    #     #Check Response code
    #     response1 = self.client.get(reverse("login:logout"))
    #     self.assertEqual(response.status_code, 200)
    #     # Check Error messages
    #     self.assertTrue('error_message' in response.context)
    #     self.assertEqual(response.context['error_message'], None)

    def test_valid_reset_password_USER_EXISTS(self):
        response = self.client.get(reverse('login:resetpassword'))
        self.assertEqual(response.status_code,200)
        response = self.client.post(reverse("login:resetpassword"),
                                    {'email': 'testing2@test.com'})
        print(response.context)
        self.assertEqual(response.context['error_message'], 'Password reset is successful. Please check your email for the new password.')

