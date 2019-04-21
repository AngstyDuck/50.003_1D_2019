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

    def test_successful_registerAndLogin(self):
        # Create account with these information then login
        create_user = 'Jackson'
        create_phoneNumber = '12345678'
        create_email = 'jackson@mail.com'
        create_password = 'password1234'

        driver = self.driver
        #Opening the link we want to test
        driver.get('http://127.0.0.1:8000/createuser/')
        #find the form element
        username = driver.find_element_by_name('username')
        phoneNumber = driver.find_element_by_name('phoneNumber')
        email = driver.find_element_by_name('email')
        password = driver.find_element_by_name('password')

        #Fill the form with data
        username.send_keys(create_user)
        time.sleep(1)
        phoneNumber.send_keys(create_phoneNumber)
        time.sleep(1)
        email.send_keys(create_email)
        time.sleep(1)
        password.send_keys(create_password)
        time.sleep(1)
        check_email_box = driver.find_element_by_css_selector("#notify_email")
        check_email_box.click()
        #time.sleep(2)
        #submitting the registration form
        submit_button = driver.find_elements_by_css_selector("button.btn")[0]
        submit_button.click()

        # check the returned result
        # assert 'Check your email' in driver.page_source
        check_registered = self.is_text_present("Please sign in")
        if check_registered == True:
            print("User has registered")

        # explicitly wait until password field is present in login page
        try:
            WebDriverWait(driver,10).until(
                EC.element_to_be_clickable((By.ID, 'id_password'))
            )
            user_login = driver.find_element_by_id('id_username')
            user_login.send_keys(create_user)
            time.sleep(3)
            password_login = driver.find_element_by_id('id_password')
            password_login.send_keys(create_password)
            time.sleep(3)
            login_button = driver.find_element_by_xpath("/html/body/form/div/button")
            login_button.click()
            time.sleep(2)
            print("User has logged in")

        except TimeoutException:
            print("ERROR: Registration invalid")
        finally:
            driver.quit()
        # check if account got signed in
        # try:
        #     WebDriverWait(driver,10).until(
        #         # find sign out button
        #         EC.element_to_be_clickable((By.XPATH,'/html/body/nav/ul/li[2]/a'))
        #     )
        #     user_sign_out = driver.find_element_by_xpath('/html/body/nav/ul/li[2]/a')
        #     user_sign_out.click()
        #
        # except NoSuchElementException:
        #     print("Login failed")
        # finally:
        #     driver.quit()

    def test_bad_Username_registerAndLogin(self):
        # Create account with these information then login
        create_user = '12###'
        create_phoneNumber = '12345678'
        create_email = 'motley@mail.com'
        create_password = 'password1234'

        driver = self.driver
        #Opening the link we want to test
        driver.get('http://127.0.0.1:8000/createuser/')
        #find the form element
        username = driver.find_element_by_name('username')
        phoneNumber = driver.find_element_by_name('phoneNumber')
        email = driver.find_element_by_name('email')
        password = driver.find_element_by_name('password')

        username.send_keys(create_user)
        time.sleep(1)
        phoneNumber.send_keys(create_phoneNumber)
        time.sleep(1)
        email.send_keys(create_email)
        time.sleep(1)
        password.send_keys(create_password)
        time.sleep(1)
        check_email_box = driver.find_element_by_css_selector("#notify_email")
        check_email_box.click()
        # time.sleep(2)
        # submitting the registration form
        submit_button = driver.find_elements_by_css_selector("button.btn")[0]
        submit_button.click()

        # check the returned result
        # assert 'Check your email' in driver.page_source
        check_registered = self.is_text_present("Please sign in")
        if check_registered == True:
            print("User has registered")

        # explicitly wait until password field is present in login page
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'id_password'))
            )
            user_login = driver.find_element_by_id('id_username')
            user_login.send_keys(create_user)
            time.sleep(3)
            password_login = driver.find_element_by_id('id_password')
            password_login.send_keys(create_password)
            time.sleep(3)
            login_button = driver.find_element_by_xpath("/html/body/form/div/button")
            login_button.click()
            time.sleep(2)
            print("User has logged in")

        except TimeoutException:
            print("ERROR: Field Input invalid")
            raise

        finally:
            driver.quit()

    def test_bad_phoneNumber_registerAndLogin(self):
        # Create account with these information then login
        create_user = 'Hilda'
        create_phoneNumber = 'a12345678'
        create_email = 'motley@mail.com'
        create_password = 'password1234'

        driver = self.driver
        #Opening the link we want to test
        driver.get('http://127.0.0.1:8000/createuser/')
        #find the form element
        username = driver.find_element_by_name('username')
        phoneNumber = driver.find_element_by_name('phoneNumber')
        email = driver.find_element_by_name('email')
        password = driver.find_element_by_name('password')

        username.send_keys(create_user)
        time.sleep(1)
        phoneNumber.send_keys(create_phoneNumber)
        time.sleep(1)
        email.send_keys(create_email)
        time.sleep(1)
        password.send_keys(create_password)
        time.sleep(1)
        check_email_box = driver.find_element_by_css_selector("#notify_email")
        check_email_box.click()
        # time.sleep(2)
        # submitting the registration form
        submit_button = driver.find_elements_by_css_selector("button.btn")[0]
        submit_button.click()

        # check the returned result
        # assert 'Check your email' in driver.page_source
        check_registered = self.is_text_present("Please sign in")
        if check_registered == True:
            print("User has registered")

        # explicitly wait until password field is present in login page
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'id_password'))
            )
            user_login = driver.find_element_by_id('id_username')
            user_login.send_keys(create_user)
            time.sleep(3)
            password_login = driver.find_element_by_id('id_password')
            password_login.send_keys(create_password)
            time.sleep(3)
            login_button = driver.find_element_by_xpath("/html/body/form/div/button")
            login_button.click()
            time.sleep(2)
            print("User has logged in")

        except TimeoutException:
            print("ERROR: Field Input invalid")
            raise

        finally:
            driver.quit()

    def test_AccountAlreadyExists_registerAndLogin(self):
        # Create account with these information then login
        create_user = 'Crew'
        create_phoneNumber = '12345678'
        create_email = 'crew@mail.com'
        create_password = 'password1234'

        driver = self.driver
        #Opening the link we want to test
        driver.get('http://127.0.0.1:8000/createuser/')
        #find the form element
        username = driver.find_element_by_name('username')
        phoneNumber = driver.find_element_by_name('phoneNumber')
        email = driver.find_element_by_name('email')
        password = driver.find_element_by_name('password')

        #Fill the form with data
        username.send_keys(create_user)
        time.sleep(1)
        phoneNumber.send_keys(create_phoneNumber)
        time.sleep(1)
        email.send_keys(create_email)
        time.sleep(1)
        password.send_keys(create_password)
        time.sleep(1)
        check_email_box = driver.find_element_by_css_selector("#notify_email")
        check_email_box.click()
        #time.sleep(2)
        #submitting the registration form
        submit_button = driver.find_elements_by_css_selector("button.btn")[0]
        submit_button.click()

        # check the returned result
        # assert 'Check your email' in driver.page_source
        check_registered = self.is_text_present("Please sign in")
        if check_registered == True:
            print("User has registered")

        # explicitly wait until password field is present in login page
        try:
            WebDriverWait(driver,10).until(
                EC.element_to_be_clickable((By.ID, 'id_password'))
            )
            user_login = driver.find_element_by_id('id_username')
            user_login.send_keys(create_user)
            time.sleep(3)
            password_login = driver.find_element_by_id('id_password')
            password_login.send_keys(create_password)
            time.sleep(3)
            login_button = driver.find_element_by_xpath("/html/body/form/div/button")
            login_button.click()
            time.sleep(2)
            print("User has logged in")

        except TimeoutException:
            print("ERROR: User already exists")
            raise
        finally:
            driver.quit()



