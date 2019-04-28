from django.test import LiveServerTestCase
from django.contrib.sessions.models import Session
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
import re


# run in Source\website --> python manage.py test createuser.tests.test_login.AccountTestCase

class AccountLoginTestCase(LiveServerTestCase):
    # To initialise the driver
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(AccountLoginTestCase, self).setUp()

    # Terminate the session
    def tearDown(self):
        self.driver.quit()
        super(AccountLoginTestCase, self).tearDown()

    # to check is  text is present
    def is_text_present(self, text):
        return str(text) in self.driver.page_source

    # Test a login with an already created account
    def test_successful_login(self):
        # login only requires username and password
        existing_user = 'Tired'
        existing_password = '1234'

        driver = self.driver
        # Open wanted link
        driver.get('http://127.0.0.1:8000/')
        # find form elements (by_name -> remember in login.html, in class tag you set name="something")
        username = driver.find_element_by_name('username')
        password = driver.find_element_by_name('password')
        # fill up the form
        username.send_keys(existing_user)
        time.sleep(1)
        password.send_keys(existing_password)
        time.sleep(1)
        # submit form
        login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
        login_button.click()

        # check the returned results
        current_url = driver.current_url
        if (current_url == 'http://127.0.0.1:8000/home/'):
            print("1. User has logged in")
            time.sleep(10)
            driver.quit()

        else:
            print("1. Unsuccessful Login")

    # Test a login with an already created User account
    def test_successful_login_user(self):
        # login only requires username and password
        existing_user = 'Tired'
        existing_password = '1234'

        driver = self.driver

        # Open wanted link
        driver.get('http://127.0.0.1:8000/')
        # find form elements (by_name -> remember in login.html, in class tag you set name="something")
        username = driver.find_element_by_name('username')
        password = driver.find_element_by_name('password')
        # fill up the form
        username.send_keys(existing_user)
        time.sleep(1)
        password.send_keys(existing_password)
        time.sleep(1)
        # submit form
        login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
        login_button.click()
        print("1. User has logged in")

        # check the returned results
        current_url = driver.current_url
        # print(driver)
        if (current_url == 'http://127.0.0.1:8000/home/'):
            #  only user account's have create ticket
            try:
                createticket_button = driver.find_element_by_link_text("Create Ticket")
                createticket_button.click()
                time.sleep(10)
                check_registered = self.is_text_present("Create a")
                if check_registered == True:
                    print("2. User has logged into User account")

            except NoSuchElementException:
                print("2. This is an admin account, something is wrong hmmm")

        else:
            print("2. Did not redirect to dashboard")

    def test_successful_login_admin(self):
        # login only requires username and password
        existing_user = 'joe'
        existing_password = "1234"

        driver = self.driver

        # Open wanted link
        driver.get('http://127.0.0.1:8000/')
        # find form elements (by_name -> remember in login.html, in class tag you set name="something")
        username = driver.find_element_by_name('username')
        password = driver.find_element_by_name('password')
        # fill up the form
        username.send_keys(existing_user)
        time.sleep(1)
        password.send_keys(existing_password)
        time.sleep(1)
        # submit form
        login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
        login_button.click()
        print("1.User has logged in")

        # check the returned results
        current_url = driver.current_url

        if (current_url == 'http://127.0.0.1:8000/home/'):
            #  only Admin account has the task card
            time.sleep(5)
            try:
                view_ticket = driver.find_element_by_link_text("View Tickets")
                view_ticket.click()
                print("2. User has logged into Admin account")


            except NoSuchElementException:
                print("2. Admin has logged into user account, hmmm something is wrong")

        else:
            print("2. Did not redirect to dashboard")

    def test_all_links_work(self):
        driver = self.driver

        # Open wanted link
        driver.get('http://127.0.0.1:8000/')
        # get all links
        for a in driver.find_elements_by_xpath('.//a'):
            print("link text: " + a.text)
            fr = a.get_attribute('href')
            print("Navigating to: " + fr)

    # test that invalid username/password tried to login w/ error messages + renetre with valid
    def test_login_invalid_info_with_message_renenter(self):
        invalid_username = 'lauren'
        invalid_password = '1234'

        driver = self.driver

        # Open wanted link
        driver.get('http://127.0.0.1:8000/')
        username = driver.find_element_by_name('username')
        password = driver.find_element_by_name('password')
        # fill up the form
        username.send_keys(invalid_username)
        time.sleep(1)
        password.send_keys(invalid_password)
        time.sleep(1)
        # submit form
        login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
        login_button.click()
        time.sleep(4)
        # ensure that page did not redirect to anywhere else
        if (driver.current_url == 'http://127.0.0.1:8000/'):
            check_errormessage = self.is_text_present("Login failure, username or password is incorrect")
            if check_errormessage == True:
                print("1. User has tried to login with an invalid account")
                time.sleep(3)
                close_message = driver.find_element_by_class_name("close")
                close_message.click()
                time.sleep(10)
                check_errormessage_now = self.is_text_present("Login failure, username or password is incorrect")
                if (check_errormessage_now == False):
                    print("2. error message closed")

                    existing_user = "testuser1"
                    existing_password = "Password123"
                    username = driver.find_element_by_name('username')
                    password = driver.find_element_by_name('password')
                    # fill up the form
                    username.send_keys(existing_user)
                    time.sleep(1)
                    password.send_keys(existing_password)
                    time.sleep(1)
                    # submit form
                    login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
                    login_button.click()

                    # check the returned results
                    current_url = driver.current_url
                    if (current_url == 'http://127.0.0.1:8000/home/'):
                        print("3. User has logged in")
                        time.sleep(10)
                        driver.quit()

                    else:
                        print("3. Unsuccessful Login")

                else:
                    print("2. issue with closing message alert")

            else:
                print("1. Wrong error/no error message")
        else:
            print("1. Not suppose to be: " + driver.current_url)