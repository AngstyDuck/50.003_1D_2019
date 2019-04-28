from createuser.models import Extended_User
from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from ticket_creation.models import Ticket_Details,Ticket,All_Tickets

class HomeViewTest(TestCase):
    def setUp(self):
        # Create an existing User
        self.client = Client()
        test_user2 = Extended_User.objects.create(username='testuser2',
                                                  password='HelloSekai123',
                                                  email='testing@test.com',
                                                  phoneNumber='12345679',
                                                  notify_email=True,
                                                  notify_sms=False)
        test_user2.set_password('HelloSekai123')
        test_user2.is_active = True
        test_user2.save()

        test_admin = Extended_User.objects.create(username='joe',
                                                  email='admin@test.com',
                                                  phoneNumber='97532134',
                                                  notify_email=True,
                                                  notify_sms=False,
                                                  is_superuser=True)
        test_admin.set_password('1234')
        test_admin.is_active = True
        test_admin.save()

        # test_ticket1 = Ticket.objects.create(ticket_id='testticket1',
        #                                      title='Help', resolved=0,
        #                                      read=0,
        #                                      description='Please help thanks',
        #                                      user='testuser2')
        # test_ticket1.save()

        # NEW ADMIN (SUPERUSER) - Username:herms, Password:9876
        # Email: herms@test.com
        # PhoneNumber: 45678901

    # test web status codes
    def test_USER_logged_in_home_status(self):
        login = self.client.post(reverse('login:index'), {'username': 'testuser2',
                                                          'password': 'HelloSekai123'})
        self.assertEqual(login.status_code, 302)

    def test_USER__wrong_password_status(self):
        login = self.client.post(reverse('login:index'),{'username':'testuser2',
                                            'password':'HellooSekai123'})
        self.assertEqual(login.status_code, 200)
        self.assertTemplateUsed(login,'login.html')

    def test_ADMIN_logged_in_home_status(self):
        login = self.client.login(username='joe', password='1234')
        response = self.client.get(reverse('home:index'))
        self.assertEqual(response.status_code, 200)

    def test_NO_LOGIN_status(self):
        response = self.client.get(reverse('login:index'))
        self.assertEqual(response.status_code, 200)

    # Test for correct template being used
    def test_NO_LOGIN_uses_correct_template(self):
        response = self.client.get(reverse('login:index'))
        self.assertTemplateUsed(response, 'login.html')

    def test_ADMIN_LOGIN_NO_TICKET_IN_DASHBOARD_uses_correct_template(self):
        login = self.client.login(username='joe', password='1234')
        # print(login)
        response = self.client.get(reverse('home:index'))
        self.assertTemplateUsed(response,'noticketadmin.html')

    def test_USER_LOGIN_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        # print(login)
        response = self.client.get(reverse('home:index'))
        self.assertTemplateUsed(response,'baseuser.html')

    def test_ADMIN_LOGIN_TICKET_IN_DASHBOARD_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        response = self.client.post(reverse('ticket_creation:create'), {
            'title': 'Help',
            'email': 'testing@test.com',
            'description': 'Please help thanks',
        })
        self.client.logout()
        login = self.client.login(username='joe', password='1234')
        # print(login)
        response = self.client.get(reverse('home:index'))
        self.assertTemplateUsed(response,'dashboardadmin.html')