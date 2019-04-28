from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  NoSuchElementException
import time
from ticket_creation.models import All_Tickets, Ticket, Ticket_Details


class EditProfileByUser(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(EditProfileByUser, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(EditProfileByUser, self).tearDown()

    def is_text_present(self, text):
        return str(text) in self.driver.page_source

    def test_EditProfileByUser(self):
        user_username = 'Tired'
        user_password = '1234'
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        username_field = driver.find_element_by_name("username")
        password_field = driver.find_element_by_name("password")
        username_field.send_keys(user_username)
        time.sleep(1)
        password_field.send_keys(user_password)
        time.sleep(1)
        login_button = driver.find_element_by_xpath("/html/body/form/div/div/div/div/div/button")
        login_button.click()
        time.sleep(2)
        print("User has logged in")

        link_profile= driver.find_element_by_link_text('Profile')
        link_profile.click()
        time.sleep(2)

        update_profile_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/header/div/div/div/div/div/div/button")
        time.sleep(1)
        update_profile_button.click()

        username_update = driver.find_element_by_xpath("/html/body/div[1]/div/div/header/div/div/div/div/div/div/div[2]/div/div/div[2]/form/div[1]/input")
        time.sleep(2)
        username_update.clear()
        username_update.send_keys("Awake")
        time.sleep(2)
        submit_detail_button = driver.find_element_by_xpath("/html/body/div[1]/div/div/header/div/div/div/div/div/div/div[2]/div/div/div[2]/form/div[8]/button[1]")
        time.sleep(1)
        submit_detail_button.click()

        expectedMessage = 'X\nEdit profile success'
        message = driver.find_element_by_xpath("/html/body/div[1]/div/div/header/div/div[1]")
        msg_text = message.text
        self.assertTrue(message)
        self.assertEqual(msg_text, expectedMessage)
        time.sleep(2)


        driver.quit()