# Testing with views is a little more complicated
# need to test more code paths: intial display, display after data validation has failed
# display after validation has suceeded. The good news is that we use the client
# for testing exactly the same way as we did for display views only

import datetime
from ticket_creation.models import All_Tickets
from ticket_creation.models import Ticket_Details
from django.test import TestCase
from django.contrib.auth.models import User
from ticket_creation.models import Ticket
from django.urls import reverse
from django.test import Client
from createuser.models import Extended_User
from ticket_creation.views import error_message_invalid_input, \
    error_message_empty_input, error_message_success,\
    error_message_forbidden_administrator,\
    error_message_forbidden_nonadministrator,\
    error_message_one_checkbox,error_message_unauthorised,\
    error_message_unknown_error

# run in Source\website --> python manage.py test ticket_creation.tests.test_view.CreateTicketInstanceViewTest


class CreateTicketInstanceViewTest(TestCase):
    @classmethod
    def setUp(self):
        self.client = Client()
        # Create an existing User
        # test_admin = User(username='joe',
        #                   is_staff=True,
        #                   email='admin@test.com',)
        #                   #phoneNumber='97532134',
        #                   #notify_email=True,
        #                   #notify_sms=False)
        # test_admin.set_password('1234')
        # test_admin.save()
        test_admin = Extended_User.objects.create(username='joe',
                                                  email='admin@test.com',
                                                  phoneNumber='97532134',
                                                  notify_email=True,
                                                  notify_sms=False,
                                                  is_superuser=True)
        test_admin.set_password('1234')
        test_admin.is_active = True
        test_admin.save()
        test_user2 = Extended_User.objects.create(username='testuser2',
                                                  password='HelloSekai123',
                                                  email='pleasedontlockthisemailthanks@gmail.com',
                                                  phoneNumber='12345679',
                                                  notify_email=True,
                                                  notify_sms=False)
        test_user2.set_password('HelloSekai123')
        test_user2.is_active = True
        test_user2.save()
        test_ticket1 = Ticket.objects.create(ticket_id='testticket1',
                                             title='Help', resolved=0,
                                             read=0,
                                             description='Please help thanks',
                                             user='testuser2')
        test_ticket1.save()

        # all_ticket = All_Tickets.objects.create(size=1, creator=0,
        #                          addressed_by=1, resolved_by=None,
        #                          read_by=1, queue_number=1,
        #                          dateTime_created=datetime.datetime.now())
        # all_ticket.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('ticket_creation:create'))
        self.assertRedirects(response,'/')

    def test_logged_in_(self):
        login = self.client.login(username='testuser2',
                                  password='HelloSekai123')
        print("Is user logged in")
        print(login)
        response = self.client.get(reverse('login:index'))
        print(response.context)
        self.assertTemplateUsed(response,'login.html')
        self.assertEqual(response.status_code,200)
        self.assertTrue('error_message' in response.context)

    def test_home_page_status_code(self):
        response = self.client.get('/ticket_creation/')
        self.assertEquals(response.status_code, 302)

    def test_create_page_status_code(self):
        response = self.client.get(reverse('ticket_creation:create'))
        self.assertEquals(response.status_code, 302)

    def test_display_page_status_code(self):
        response = self.client.get(reverse('ticket_creation:display'))
        self.assertEquals(response.status_code, 302)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('ticket_creation:create'))
        self.assertEquals(response.status_code, 302)

    def test_SUCCESS_logged_in_create_ticket(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        response = self.client.post(reverse('ticket_creation:create'), {
                                                                        'title': 'Help',
                                                                        'description': 'Please help thanks',
                                                                        })
        # print(response)
        # print("@@@")
        # print(response.context)
        self.assertTrue(response.status_code,200)
        self.assertTrue('error_message' in response.context)
        self.assertEqual(response.context["error_message"], error_message_success)

    def test_FAILURE_INVALID_TITLE_logged_in_create_ticket(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        response = self.client.post(reverse('ticket_creation:create'), {
                                                                        'title': '@Help',
                                                                        'email': 'testing@test.com',
                                                                        'description': 'Please help thanks',
                                                                        })
        # print(response.context)
        # print(response.context['error_message'])
        self.assertTrue(response.status_code,200)
        self.assertNotEqual(error_message_invalid_input, response.context["error_message"])

    def test_FAILURE_INVALID_DESCRIPTION_logged_in_create_ticket(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        response = self.client.post(reverse('ticket_creation:create'), {
                                                                        'title': 'Help',
                                                                        'email': 'testing@test.com',
                                                                        'description': '@Please help thanks',
                                                                        })


        # print(response.context)
        # print(response.context['error_message'])
        self.assertTrue(response.status_code,200)
        self.assertNotEqual(response.context["error_message"], error_message_invalid_input)

    def test_FAILURE_INVALID_TITLE_INVALID_DESCRIPTION_logged_in_create_ticket(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        response = self.client.post(reverse('ticket_creation:create'), {
                                                                        'title': '#Help#',
                                                                        'email': 'testing@test.com',
                                                                        'description': '#Please help thanks#',
                                                                        })
        # print(response.context)
        # print(response.context['error_message'])
        self.assertTrue(response.status_code,200)
        self.assertNotEqual(response.context["error_message"], error_message_invalid_input)

    def test_FAILURE_INVALID_EMAIL_logged_in_create_ticket(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        response = self.client.post(reverse('ticket_creation:create'), {
                                                                        'title': 'Help',
                                                                        'email': 'testing@@test.com',
                                                                        'description': 'Please help thanks',
                                                                        })
        # print(response.context)
        # print(response.context['error_message'])
        self.assertTrue(response.status_code,200)
        self.assertNotEqual(response.context["error_message"], error_message_invalid_input)

    def test_display_ticket_TO_ADMIN(self):
        login = self.client.login(username='joe', password='1234')
        response = self.client.get(reverse('ticket_creation:display'))
        self.assertEqual(response.status_code,200)

    def test_display_ticket_TO_USER(self):
        login = self.client.login(username='testuser2', password='HelloSekai123')
        response = self.client.get(reverse('ticket_creation:display'))
        self.assertEqual(response.status_code, 403)
        # self.assertRedirects(response, reverse('home:index'))

    # def test_display_ticket_context(self):
    #     login = self.client.login(username='testuser2', password='HelloSekai123')
    #     response = self.client.post(reverse('ticket_creation:create'), {
    #         'title': 'Help',
    #         'email': 'testing@test.com',
    #         'description': 'Please help thanks',
    #     })
    #     self.client.logout()
    #     login = self.client.login(username='joe', password='1234')
    #     response = self.client.get(reverse('ticket_creation:display'))
    #     # print(response.context)
    #     self.assertEqual(response.status_code, 302)
    #     # self.assertRedirects(response, reverse('home:index'))

    # def test_admin_reply_ticket(self):
    #     login = self.client.login(username='testuser2', password='HelloSekai123')
    #     response = self.client.post(reverse('ticket_creation:create'), {
    #         'title': 'Help',
    #         'description': 'Please help thanks',
    #     })
    #
    #     self.client.logout()
    #     login = self.client.login(username='joe', password='1234')
    #     # print(login)
    #     # print(All_Tickets.objects.get_queryset())
    #     response = self.client.post('/ticket_creation/detail/?id={}'.format(Ticket.objects.get(pk=1).id),{
    #         'description': "You will be found",
    #     })
    #     self.assertEqual(response.status_code, 302)
    #
    # def test_admin_resolve_ticket(self):
    #     login = self.client.login(username='testuser2', password='HelloSekai123')
    #     print(login)
    #     response = self.client.post(reverse('ticket_creation:create'), {
    #         'title': 'Help',
    #         'description': 'Please help thanks',
    #     })
    #     self.client.logout()
    #     login = self.client.login(username='joe', password='1234')
    #     # print(login)
    #     # print(All_Tickets.objects.get_queryset())
    #     response = self.client.get(reverse('ticket_creation:resolve'))
    #     self.assertEqual(response.status_code, 302)

    def test_admin_delete_tickets(self):
        login = self.client.login()

    # def test_get_details(self):
    #     # login user first to create a ticket
    #     login = self.client.login(username='testuser2', password='HelloSekai123')
    #     response = self.client.post(reverse('ticket_creation:create'), {
    #         'title': 'Help',
    #         'email': 'testing@test.com',
    #         'description': 'Please help thanks',
    #     })
    #     logout = self.client.logout()
    #     # logins admin
    #     login = self.client.login(username='joe', password='1234')
    #     request = self.client.get(reverse('ticket_creation:display'))
    #     print(request)
    #     test_id = request.user.id
    #     response = self.client.get(reverse("ticket_creation:detail")+"?id={0}".format(test_id))
    #     print(response)

        # id_test = 1
        # response = self.client.get('/ticket_creation/detail/?id={}'.format(id_test))
        # print(response.content)
        # response = self.client.get(reverse("ticket_creation:display"))
        # self.assertEqual(response.status_code, 302)
        # # print(response)
        # item = Ticket.objects.all().filter(id=id_test)
        # print(item[0].read)
        # self.assertTrue(response.context['item'], item[0])
