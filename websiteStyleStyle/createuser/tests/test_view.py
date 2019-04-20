
#Testing with views is a little more complicated
#need to test more code paths: intial display, display after data validation has failed
#display after validation has suceeded. The good news is that we use the client
#for testing exactly the same way as we did for display views only

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from createuser.views import error_message_user_exist, error_message_empty_input


class CreateUserInstanceViewtest(TestCase):
    def setUp(self):
        # Create an existing User
        test_user1 = User.objects.create(username='testuser1', password='HelloWorld123', email='test@test.com')
        # test_user1.is_active = True
        test_user1.save()

    # Test for GET request
    def test_redirect_to_new_form(self):
        response = self.client.get(reverse('createuser:index'))
        self.assertEqual(response.status_code, 200)
        # self.assertTrue(response.startswith('/createuser/'))

    def test_redirect_after_sucessful_creation(self):
        response = self.client.post(reverse('createuser:index'),{'username':'testuser2',
                                                                  'password':'HelloKitty123',
                                                                  'email': 'testtest@test.com'} )
        #since to such user has been created, should redirect to login page
        self.assertRedirects(response, reverse('login:index'))


    #Testing for POST request
    def test_redirect_if_username_taken(self):
        response = self.client.post(reverse('createuser:index'), {'username':'testuser1',
                                                                  'password':'Helloworld123',
                                                                  'email': 'test@test.com'})
        #since test_user1 already exist, no redirection remain on the same page
        self.assertTrue('error_message' in response.context)
        # Check that the right Error Message is displayed
        self.assertEqual(response.context['error_message'], error_message_user_exist)


    def test_submit_empty_form(self):
        response = self.client.post(reverse('createuser:index'),{'username':None,
                                                                  'password':None,
                                                                  'email':None} )
        self.assertTrue('error_message' in response.context)
        # Check that the right Error Message is displayed
        self.assertEqual(response.context['error_message'], error_message_empty_input)



    def test_form_invalid_password(self):
        response = self.client.post(reverse('createuser:index'), {'username': 'HappyDay1',
                                                                  'password': None,
                                                                  'email': 'test.test@gmail.com'})
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('createuser:index'))
        self.assertTrue('error_message' in response.context)
        # Check that the right Error Message is displayed
        self.assertEqual(response.context['error_message'], error_message_empty_input)


    def test_form_invalid_email(self):
        response = self.client.post(reverse('createuser:index'), {'username': 'HappyDay1',
                                                                  'password': 'passWord123',
                                                                  'email': None})
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('createuser:index'))
        self.assertTrue('error_message' in response.context)
        # Check that the right Error Message is displayed
        self.assertEqual(response.context['error_message'], error_message_empty_input)


    def test_uses_correct_template(self):
        response = self.client.get('/createuser/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createuser/user.html')