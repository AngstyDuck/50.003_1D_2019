from django.test import LiveServerTestCase
from django.contrib.sessions.models import Session
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
import os

# run in Source\website --> python manage.py test createuser.tests.test_dashboard.AccountTestCase

class AccountTestCase(LiveServerTestCase):
    # To initialise the driver
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(AccountTestCase, self).setUp()
        
    # Terminate the session
    def tearDown(self):
        self.driver.quit()
        super(AccountTestCase, self).tearDown()

    # to check is  text is present
    def is_text_present(self, text):
        return str(text) in self.driver.page_source

    # def test_logout(self):
    #     # login only requires username and password
    #     existing_user = 'testuser1'
    #     existing_password = 'Password123'

    #     driver = self.driver
    #     # Open wanted link
    #     driver.get('http://127.0.0.1:8000/')
    #     # find form elements (by_name -> remember in login.html, in class tag you set name="something")
    #     username = driver.find_element_by_name('username')
    #     password = driver.find_element_by_name('password')
    #     # fill up the form
    #     username.send_keys(existing_user)
    #     time.sleep(1)
    #     password.send_keys(existing_password)
    #     time.sleep(1)
    #     #submit form
    #     login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
    #     login_button.click()
    #     time.sleep(2)

    #     logout_button = driver.find_element_by_name("logout")
    #     print(logout_button.get_attribute('href'))
    #     logout_button.click()
    #     time.sleep(1)
    #     logout_confirm = driver.find_element_by_css_selector("#logoutModal > div > div > div.modal-footer > a")
    #     logout_confirm.click()
    #     # check that it is the login page
    #     if (driver.current_url == "http://127.0.0.1:8000/"):
    #         print("successful logout")
    #         time.sleep(3)
    #         driver.quit()
    #     else:
    #         print("Did not manage to logout")
        
        


    # phase 1. Test that goes from 1. Trying to login, invalid username due to to typo, get error message, close error message, login successful, 
    # phase 2. create ticket, check if ticket has been showed in dashboard
    # phase 3. clicks on ticket and enetr forum, send 2 types of messages, one pure text and one is with file link
    # phase 4. user logs out and admin now logs in
    # pahse 5. admin clicks on that ticket and enters the chat and sends back a response
    # phase 6. user should see the new message from admin

    def test_demo_full(self):
        # setting up account details
        invalid_username = 'lauren'
        valid_username = 'twobowlsofgrace'
        valid_password = 'Password123'

        valid_adminuser = 'testadmin1'
        valid_adminpassword = "Tonight'sdinner"

        driver = self.driver
        driver.get('http://127.0.0.1:8000/')

        # phase1
        username = driver.find_element_by_name('username')
        password = driver.find_element_by_name('password')
        # fill up with invalid username
        username.send_keys(invalid_username)
        time.sleep(1)
        password.send_keys(valid_password)
        time.sleep(1)
        #submit form
        login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
        login_button.click()
        time.sleep(4)

        if (driver.current_url =='http://127.0.0.1:8000/' ):
            check_errormessage = self.is_text_present("Login failure, username or password is incorrect")
            if check_errormessage == True:
                print("Phase1: 1. User has tried to login with invalid information")
                time.sleep(3)
                close_message = driver.find_element_by_class_name("close")
                close_message.click()
                time.sleep(10)
                check_errormessage_now = self.is_text_present("Login failure, username or password is incorrect")
                if (check_errormessage_now == False):
                    print("Phase1: 2. error message closed")

                    username = driver.find_element_by_name('username')
                    password = driver.find_element_by_name('password')
                    # fill up the form
                    username.send_keys(valid_username)
                    time.sleep(1)
                    password.send_keys(valid_password)
                    time.sleep(1)
                    #submit form
                    login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
                    login_button.click()

                    # check the returned results
                    current_url = driver.current_url
                    if (current_url == 'http://127.0.0.1:8000/home/'):
                        print("Phase1: 3. User has logged in")
                        time.sleep(10)
                        # driver.quit()


                        # phase 2
                        # User clicks Create Ticket link to create ticket
                        link_create_ticket = driver.find_element_by_link_text('Create Ticket')
                        link_create_ticket.click()
                        time.sleep(2)

                        ticket_title = 'Missing Function, unable to launch system'
                        ticket_description = 'I cant seem to find this fnction. Not sure if my version is outdated'

                        ticket_title_field = driver.find_element_by_name("title")
                        print("Phase2: 1. Redirected to Create ticket Page")
                        ticket_title_field.send_keys(ticket_title)
                        time.sleep(1)
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        ticket_description_field = driver.find_element_by_id('description')

                        ticket_description_field.send_keys(ticket_description)
                        time.sleep(1)

                        ticket_create_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/form/div/div/div/div/div/button")
                        ticket_create_button.click()
                        time.sleep(3)
                        expectedMessage = 'x\nTicket creation success'
                        message = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div")
                        msg_text = message.text
                        self.assertTrue(message)
                        # self.assertEqual(msg_text, expectedMessage)
                        if (msg_text == expectedMessage):
                            print("Phase2: 2. Ticket Successfullly created")

                            close_notif = driver.find_element_by_xpath("/html/body/div[1]/div/div/div/div/button")
                            close_notif.click()
                            time.sleep(2)
                            link_create_ticket = driver.find_element_by_link_text('Dashboard')
                            link_create_ticket.click()
                            time.sleep(2)
                            link_new_ticket = driver.find_element_by_link_text(ticket_title)
                            print("Phase2: 3. Redirected to Dashboard and find ticket")
                            link_new_ticket.click()
                            time.sleep(2)

                            # phase 3 go click forum and send message
                            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            time.sleep(2)
                            # input message 
                            reply_message_field = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[2]/form/div/div/div/div[1]/input")
                            reply_message = 'I really appreciate your reply on this matter'
                            reply_message_field.send_keys(reply_message)
                            submit_reply_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[2]/form/div/div/div/button")
                            submit_reply_button.click()
                            time.sleep(2)
                            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                            time.sleep(2)

                            check_reply_sent = self.is_text_present(reply_message)
                            if check_reply_sent:
                                print("Phase3: 1. Reply has been successfully posted")
                                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                                message_attach = "Attached a file"
                                reply_message_field = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[2]/form/div/div/div/div[1]/input")
                                reply_message_field.send_keys(message_attach)
                                attach_file_button = driver.find_element_by_name('file')
                                attach_file_button.send_keys(os.getcwd()+ "\\static\\img\\light-grey-terrazzo.png")

                                time.sleep(3)
                                submit_reply_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[2]/form/div/div/div/button")
                                submit_reply_button.click()
                                time.sleep(2)
                                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                                time.sleep(3)
                                check_reply_sent = self.is_text_present(message_attach)
                                if check_reply_sent:
                                    print("Phase3: 2. Reply with file attachment has been successfully posted")
                                    # phase 4
                                    logout_button = driver.find_element_by_name("logout")
                                    # print(logout_button.get_attribute('href'))
                                    logout_button.click()
                                    time.sleep(1)
                                    logout_confirm = driver.find_element_by_css_selector("#logoutModal > div > div > div.modal-footer > a")
                                    print("Phase4: 1. Confirm Logout")
                                    logout_confirm.click()
                                    # check that it is the login page
                                    if (driver.current_url == "http://127.0.0.1:8000/"):
                                        print("Phase4: 2. User Successfully Logged-out")
                                        time.sleep(3)

                                        # Admin now logs in
                                        username = driver.find_element_by_name('username')
                                        password = driver.find_element_by_name('password')
                                        # fill up tcurrent_window_handle
                                        username.send_keys(valid_adminuser)
                                        time.sleep(1)
                                        password.send_keys(valid_adminpassword)
                                        time.sleep(1)
                                        #submit form
                                        login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
                                        login_button.click()
                                        if (driver.current_url == 'http://127.0.0.1:8000/home/'):
                                            #  only Admin account has the task card
                                            time.sleep(3)
                                            try:
                                                view_ticket = driver.find_element_by_link_text("View Tickets")
                                                print("Phase4: 3. Admin has logged into Admin account")

                                                # phase 5
                                                # admin looks for ticket that was just created -> for simplicity sake, will look for title
                                                find_ticket = driver.find_element_by_link_text(ticket_title) # the link text should b ethe ticket na,e -> to hard code this
                                                # print("Manage to find element is where it all went wrong")
                                                find_ticket.click()
                                                check_right_forum = self.is_text_present(ticket_title)
                                                if (check_right_forum == True):
                                                    print("Phase5: 1. Admin has clicked on to the right ticket")
                                                    time.sleep(2)
                                                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                                                    time.sleep(2)
                                                    # input message 
                                                    reply_message_field_admin = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[2]/form/div/div/div/div[1]/input")
                                                    reply_message_admin = 'Hi, I am the admin, How can I help you?'
                                                    reply_message_field_admin.send_keys(reply_message_admin)
                                                    submit_reply_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div[2]/form/div/div/div/button")
                                                    submit_reply_button.click()
                                                    time.sleep(2)
                                                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                                                    time.sleep(2)

                                                    check_reply_sent = self.is_text_present(reply_message_admin)
                                                    if (check_reply_sent == True):
                                                        print("Phase5: 2. Admin successfully replied to thread ")
                                                        #  log out admin
                                                        logout_button = driver.find_element_by_name("logout")
                                                        # print(logout_button.get_attribute('href'))
                                                        logout_button.click()
                                                        time.sleep(1)
                                                        logout_confirm = driver.find_element_by_css_selector("#logoutModal > div > div > div.modal-footer > a")
                                                        print("Phase5: 3. Admin Confirm Logout")
                                                        logout_confirm.click()
                                                        if (driver.current_url == "http://127.0.0.1:8000/" ):
                                                            print("Phase5: 4. Admin Successfully Logged-out")
                                                            time.sleep(3)
                                                            # phase 6 user log back in
                                                            username = driver.find_element_by_name('username')
                                                            password = driver.find_element_by_name('password')
                                                            # fill up the form
                                                            username.send_keys(valid_username)
                                                            time.sleep(1)
                                                            password.send_keys(valid_password)
                                                            time.sleep(1)
                                                            #submit form
                                                            login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
                                                            login_button.click()

                                                            if (driver.current_url == 'http://127.0.0.1:8000/home/' ):
                                                                print("Phase6: 1. User has managed to log back in")
                                                                find_ticket_after = driver.find_element_by_link_text(ticket_title)
                                                                find_ticket_after.click()
                                                                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                                                                check_reply_received = self.is_text_present(reply_message_admin)
                                                                if (check_reply_received == True):
                                                                    print("Phase6: 2. User has succssfully received ticket!")
                                                                    print("----END OF SYSTEM TEST SUCCESS----")
                                                                    driver.quit()
                                                                else:
                                                                    print("Phase6: 2. User did not succssfully received ticket!")




                                                            else:
                                                                print("Phase6: 1. User has did not manage to log back in")



                                                        else:
                                                            print("Phase5: 4. Admin did not manage to log out")


                                                    else:
                                                        print("Phase5: 2. Admin did not manage to reply to ticket")

                                                    
                                                else:
                                                    print("Phase5: 1. Admin did not click on the right ticket")
                                                    time.sleep(2)



                                            except NoSuchElementException:
                                                print("Phase4: 3. Admin has logged into user account, hmmm something is wrong")

                                        else:
                                            print("Phase4: 2. User Did not Manage to logout")

                                else:
                                    print("Phase3: 2. Reply with file attachment is not successful")


                            else:
                                print("Phase3: 1.Reply was not posted")


                        else:
                            print("Phase2: 2. Ticket was not created successfully")

                    else:
                        print("Phase1: 3. Unsuccessful Login")

                else:
                    print("Phase1: 2. issue with closing message alert")
                
            else:
                print("Phase1: 1. Wrong error/no error message")
        else:
            print("Phase: 1. Not suppose to be: " + driver.current_url)


