from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time

# run in Source\website --> python manage.py test createuser.tests.test_system.AccountTestCase


class AccountTestCase(LiveServerTestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()
        super(AccountTestCase, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(AccountTestCase, self).tearDown()

    def is_text_present(self, text):
        return str(text) in self.driver.page_source

    def test_demo_full(self):
        # setting up account details
        invalid_username = 'lauren'
        valid_username = 'Tired'
        valid_password = '1234'

        valid_adminuser = 'joe'
        valid_adminpassword = "1234"

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
        # submit form
        login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
        login_button.click()
        time.sleep(4)

        if (driver.current_url == 'http://127.0.0.1:8000/'):
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
                    # submit form
                    login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
                    login_button.click()

                    # check the returned results
                    current_url = driver.current_url
                    if (current_url == 'http://127.0.0.1:8000/home/'):
                        print("Phase1: 3. User has logged in")
                        time.sleep(10)
                        # driver.quit()

                        # phase 2

                        # phase 3

                        # phase 4
                        logout_button = driver.find_element_by_name("logout")
                        # print(logout_button.get_attribute('href'))
                        logout_button.click()
                        time.sleep(1)
                        logout_confirm = driver.find_element_by_css_selector(
                            "#logoutModal > div > div > div.modal-footer > a")
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
                            # submit form
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
                                    find_ticket = driver.find_element_by_link_text(
                                        "Unable to set Jquery")  # the link text should b ethe ticket na,e -> to hard code this
                                    find_ticket.click()
                                    check_right_forum = self.is_text_present("Re: Unable to set Jquery")
                                    if (check_right_forum == True):
                                        print("Phase5: 1. Admin has clicked on to the right ticket")
                                        time.sleep(2)

                                    else:
                                        print("Phase5: 1. Admin did not click on the right ticket")
                                    time.sleep(2)



                                except NoSuchElementException:
                                    print("Phase4: 3. Admin has logged into user account, hmmm something is wrong")

                        else:
                            print("Phase4: 2. User Did not Manage to logout")



                    else:
                        print("Phase1: 3. Unsuccessful Login")

                else:
                    print("Phase1: 2. issue with closing message alert")

            else:
                print("Phase1: 1. Wrong error/no error message")
        else:
            print("Phase: 1. Not suppose to be: " + driver.current_url)





    # def test_successful_registerAndLogin(self):
    #     # Create account with these information then login
    #     create_user = 'Jackson'
    #     create_phoneNumber = '12345678'
    #     create_email = 'jackson@mail.com'
    #     create_password = 'password1234'
    #
    #     driver = self.driver
    #     #Opening the link we want to test
    #     driver.get('http://127.0.0.1:8000/createuser/')
    #     #find the form element
    #     username = driver.find_element_by_name('username')
    #     phoneNumber = driver.find_element_by_name('phoneNumber')
    #     email = driver.find_element_by_name('email')
    #     password = driver.find_element_by_name('password')
    #
    #     #Fill the form with data
    #     username.send_keys(create_user)
    #     time.sleep(1)
    #     phoneNumber.send_keys(create_phoneNumber)
    #     time.sleep(1)
    #     email.send_keys(create_email)
    #     time.sleep(1)
    #     password.send_keys(create_password)
    #     time.sleep(1)
    #     check_email_box = driver.find_element_by_css_selector("#notify_email")
    #     check_email_box.click()
    #     #time.sleep(2)
    #     #submitting the registration form
    #     submit_button = driver.find_elements_by_css_selector("button.btn")[0]
    #     submit_button.click()
    #
    #     # check the returned result
    #     # assert 'Check your email' in driver.page_source
    #     check_registered = self.is_text_present("Please sign in")
    #     if check_registered == True:
    #         print("User has registered")
    #
    #     # explicitly wait until password field is present in login page
    #     try:
    #         WebDriverWait(driver,10).until(
    #             EC.element_to_be_clickable((By.ID, 'id_password'))
    #         )
    #         user_login = driver.find_element_by_id('id_username')
    #         user_login.send_keys(create_user)
    #         time.sleep(3)
    #         password_login = driver.find_element_by_id('id_password')
    #         password_login.send_keys(create_password)
    #         time.sleep(3)
    #         login_button = driver.find_element_by_xpath("/html/body/form/div/button")
    #         login_button.click()
    #         time.sleep(2)
    #         print("User has logged in")
    #
    #     except TimeoutException:
    #         print("ERROR: Registration invalid")
    #     finally:
    #         driver.quit()
    #     # check if account got signed in
    #     # try:
    #     #     WebDriverWait(driver,10).until(
    #     #         # find sign out button
    #     #         EC.element_to_be_clickable((By.XPATH,'/html/body/nav/ul/li[2]/a'))
    #     #     )
    #     #     user_sign_out = driver.find_element_by_xpath('/html/body/nav/ul/li[2]/a')
    #     #     user_sign_out.click()
    #     #
    #     # except NoSuchElementException:
    #     #     print("Login failed")
    #     # finally:
    #     #     driver.quit()
    #
    # def test_bad_Username_registerAndLogin(self):
    #     # Create account with these information then login
    #     create_user = '12###'
    #     create_phoneNumber = '12345678'
    #     create_email = 'motley@mail.com'
    #     create_password = 'password1234'
    #
    #     driver = self.driver
    #     #Opening the link we want to test
    #     driver.get('http://127.0.0.1:8000/createuser/')
    #     #find the form element
    #     username = driver.find_element_by_name('username')
    #     phoneNumber = driver.find_element_by_name('phoneNumber')
    #     email = driver.find_element_by_name('email')
    #     password = driver.find_element_by_name('password')
    #
    #     username.send_keys(create_user)
    #     time.sleep(1)
    #     phoneNumber.send_keys(create_phoneNumber)
    #     time.sleep(1)
    #     email.send_keys(create_email)
    #     time.sleep(1)
    #     password.send_keys(create_password)
    #     time.sleep(1)
    #     check_email_box = driver.find_element_by_css_selector("#notify_email")
    #     check_email_box.click()
    #     # time.sleep(2)
    #     # submitting the registration form
    #     submit_button = driver.find_elements_by_css_selector("button.btn")[0]
    #     submit_button.click()
    #
    #     # check the returned result
    #     # assert 'Check your email' in driver.page_source
    #     check_registered = self.is_text_present("Please sign in")
    #     if check_registered == True:
    #         print("User has registered")
    #
    #     # explicitly wait until password field is present in login page
    #     try:
    #         WebDriverWait(driver, 10).until(
    #             EC.element_to_be_clickable((By.ID, 'id_password'))
    #         )
    #         user_login = driver.find_element_by_id('id_username')
    #         user_login.send_keys(create_user)
    #         time.sleep(3)
    #         password_login = driver.find_element_by_id('id_password')
    #         password_login.send_keys(create_password)
    #         time.sleep(3)
    #         login_button = driver.find_element_by_xpath("/html/body/form/div/button")
    #         login_button.click()
    #         time.sleep(2)
    #         print("User has logged in")
    #
    #     except TimeoutException:
    #         print("ERROR: Field Input invalid")
    #         raise
    #
    #     finally:
    #         driver.quit()
    #
    # def test_bad_phoneNumber_registerAndLogin(self):
    #     # Create account with these information then login
    #     create_user = 'Hilda'
    #     create_phoneNumber = 'a12345678'
    #     create_email = 'motley@mail.com'
    #     create_password = 'password1234'
    #
    #     driver = self.driver
    #     #Opening the link we want to test
    #     driver.get('http://127.0.0.1:8000/createuser/')
    #     #find the form element
    #     username = driver.find_element_by_name('username')
    #     phoneNumber = driver.find_element_by_name('phoneNumber')
    #     email = driver.find_element_by_name('email')
    #     password = driver.find_element_by_name('password')
    #
    #     username.send_keys(create_user)
    #     time.sleep(1)
    #     phoneNumber.send_keys(create_phoneNumber)
    #     time.sleep(1)
    #     email.send_keys(create_email)
    #     time.sleep(1)
    #     password.send_keys(create_password)
    #     time.sleep(1)
    #     check_email_box = driver.find_element_by_css_selector("#notify_email")
    #     check_email_box.click()
    #     # time.sleep(2)
    #     # submitting the registration form
    #     submit_button = driver.find_elements_by_css_selector("button.btn")[0]
    #     submit_button.click()
    #
    #     # check the returned result
    #     # assert 'Check your email' in driver.page_source
    #     check_registered = self.is_text_present("Please sign in")
    #     if check_registered == True:
    #         print("User has registered")
    #
    #     # explicitly wait until password field is present in login page
    #     try:
    #         WebDriverWait(driver, 10).until(
    #             EC.element_to_be_clickable((By.ID, 'id_password'))
    #         )
    #         user_login = driver.find_element_by_id('id_username')
    #         user_login.send_keys(create_user)
    #         time.sleep(3)
    #         password_login = driver.find_element_by_id('id_password')
    #         password_login.send_keys(create_password)
    #         time.sleep(3)
    #         login_button = driver.find_element_by_xpath("/html/body/form/div/button")
    #         login_button.click()
    #         time.sleep(2)
    #         print("User has logged in")
    #
    #     except TimeoutException:
    #         print("ERROR: Field Input invalid")
    #         raise
    #
    #     finally:
    #         driver.quit()
    #
    # def test_AccountAlreadyExists_registerAndLogin(self):
    #     # Create account with these information then login
    #     create_user = 'Crew'
    #     create_phoneNumber = '12345678'
    #     create_email = 'crew@mail.com'
    #     create_password = 'password1234'
    #
    #     driver = self.driver
    #     #Opening the link we want to test
    #     driver.get('http://127.0.0.1:8000/createuser/')
    #     #find the form element
    #     username = driver.find_element_by_name('username')
    #     phoneNumber = driver.find_element_by_name('phoneNumber')
    #     email = driver.find_element_by_name('email')
    #     password = driver.find_element_by_name('password')
    #
    #     #Fill the form with data
    #     username.send_keys(create_user)
    #     time.sleep(1)
    #     phoneNumber.send_keys(create_phoneNumber)
    #     time.sleep(1)
    #     email.send_keys(create_email)
    #     time.sleep(1)
    #     password.send_keys(create_password)
    #     time.sleep(1)
    #     check_email_box = driver.find_element_by_css_selector("#notify_email")
    #     check_email_box.click()
    #     #time.sleep(2)
    #     #submitting the registration form
    #     submit_button = driver.find_elements_by_css_selector("button.btn")[0]
    #     submit_button.click()
    #
    #     # check the returned result
    #     # assert 'Check your email' in driver.page_source
    #     check_registered = self.is_text_present("Please sign in")
    #     if check_registered == True:
    #         print("User has registered")
    #
    #     # explicitly wait until password field is present in login page
    #     try:
    #         WebDriverWait(driver,10).until(
    #             EC.element_to_be_clickable((By.ID, 'id_password'))
    #         )
    #         user_login = driver.find_element_by_id('id_username')
    #         user_login.send_keys(create_user)
    #         time.sleep(3)
    #         password_login = driver.find_element_by_id('id_password')
    #         password_login.send_keys(create_password)
    #         time.sleep(3)
    #         login_button = driver.find_element_by_xpath("/html/body/form/div/button")
    #         login_button.click()
    #         time.sleep(2)
    #         print("User has logged in")
    #
    #     except TimeoutException:
    #         print("ERROR: User already exists")
    #         raise
    #     finally:
    #         driver.quit()



# run in Source\website --> python manage.py test createuser.tests.test_register.AccountTestCase

class AccountRegisterTestCase(LiveServerTestCase):
    # To initialise the driver
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(AccountRegisterTestCase, self).setUp()

        # Terminate the session

    def tearDown(self):
        self.driver.quit()
        super(AccountRegisterTestCase, self).tearDown()

        # to check is  text is present

    def is_text_present(self, text):
        return str(text) in self.driver.page_source

    def test_login_register_login(self):
        create_user = 'testuser16'
        create_phoneNumber = '12345678'
        create_email = 'testuser15@mail.com'
        create_password = 'Password123'

        driver = self.driver
        # Open wanted link
        driver.get('http://127.0.0.1:8000/')

        # get and click on register link
        view_ticket = driver.find_element_by_link_text("Don't have account? Register Here!")
        view_ticket.click()
        time.sleep(2)
        print(driver.current_url)

        # find the form element
        username = driver.find_element_by_name('username')
        phoneNumber = driver.find_element_by_name('phoneNumber')
        email = driver.find_element_by_name('email')
        password = driver.find_element_by_name('password')
        notify_email = driver.find_element_by_name('notify_email')
        notify_sms = driver.find_element_by_name('notify_sms')

        #  fill up fomr
        username.send_keys(create_user)
        time.sleep(2)
        phoneNumber.send_keys(create_phoneNumber)
        time.sleep(2)
        email.send_keys(create_email)
        time.sleep(2)
        password.send_keys(create_password)
        time.sleep(2)
        notify_email.click()
        notify_sms.click()
        time.sleep(3)

        # submit form
        register_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div[2]/div/button")
        register_button.click()
        if (driver.current_url == "http://127.0.0.1:8000/createuser/"):
            print("1. registration unsuccessful")
            driver.quit()
        if (driver.current_url == "http://127.0.0.1:8000/"):
            print("1. successful registration")
            time.sleep(2)

            # start loging in
            username = driver.find_element_by_name('username')
            password = driver.find_element_by_name('password')
            # fill up the form
            username.send_keys(create_user)
            time.sleep(1)
            password.send_keys(create_password)
            time.sleep(1)
            # submit login form
            login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
            login_button.click()

            current_url = driver.current_url
            if (current_url == 'http://127.0.0.1:8000/home/'):
                print("2. User has logged in")
                time.sleep(10)
                driver.quit()

            else:
                print("2. Unsuccessful Login")

    def test_find_all_links(self):
        driver = self.driver

        # Open wanted link
        driver.get('http://127.0.0.1:8000/createuser/')
        # get all links
        for a in driver.find_elements_by_xpath('.//a'):
            print("link text: " + a.text)
            fr = a.get_attribute('href')
            print("Navigating to: " + fr)
            if (fr == "http://127.0.0.1:8000/"):
                print("linked to the right page")
            else:
                print("error")

    def test_submit_empty_form_with_message(self):
        driver = self.driver

        # Open wanted link
        driver.get('http://127.0.0.1:8000/createuser/')
        # click register button
        register_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div[2]/div/button")
        register_button.click()
        time.sleep(4)
        if (driver.current_url == 'http://127.0.0.1:8000/createuser/'):
            check_errormessage = self.is_text_present("Please fill in all input fields")
            if check_errormessage == True:
                print("User has tried to submit an empty form")
                time.sleep(3)
            else:
                print("Wrong error/no error message")
        else:
            print("Not suppose to be: " + driver.current_url)



