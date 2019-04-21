from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import  NoSuchElementException
import time


class CreateTicketByUser(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(CreateTicketByUser, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(CreateTicketByUser, self).tearDown()

    def test_CreateTicketByUser(self):
        user_username= 'Tired'
        user_password = '1234'
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login/")
        username_field = driver.find_element_by_name("username")
        password_field = driver.find_element_by_name("password")
        username_field.send_keys(user_username)
        time.sleep(1)
        password_field.send_keys(user_password)
        time.sleep(1)
        login_button = driver.find_element_by_xpath("/html/body/form/div/button")
        login_button.click()
        time.sleep(2)
        print("User has logged in")

        # User has logged in
        # User clicks Create Ticket link to create ticket
        link_create_ticket = driver.find_element_by_link_text('Create Ticket')
        link_create_ticket.click()

        ticket_email = 'tired@mail.com'
        ticket_title = 'Help'
        ticket_description = 'Send Help'

        email_field = driver.find_element_by_name('email')
        ticket_title_field = driver.find_element_by_name('title')
        # wait = WebDriverWait(driver, 20)
        # wait.until(EC.visibility_of_element_located((By.NAME, "description")))
        ticket_description_field = driver.find_element_by_tag_name('textarea')
        # driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(5)
        email_field.send_keys(ticket_email)
        time.sleep(1)
        ticket_title_field.send_keys(ticket_title)
        time.sleep(1)

        # ticket_description_field.click()
        ticket_description_field.send_keys(ticket_description)
        time.sleep(1)
        create_ticket_button = driver.find_element_by_xpath("/html/body/div/div[2]/form/button")
        create_ticket_button.click()
        expectedMessage = "Ticket creation success"
        message = driver.find_element_by_xpath("/html/body/ul/li/div")
        self.assertTrue(message)

        driver.quit()


class ViewTicketByAdmin(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        super(ViewTicketByAdmin, self).setUp()

    def tearDown(self):
        self.driver.quit()
        super(ViewTicketByAdmin, self).tearDown()

    def test_ViewTicketByAdmin(self):
        user_username = 'joe'
        user_password = '1234'
        driver = self.driver
        driver.get("http://127.0.0.1:8000/login/")
        username_field = driver.find_element_by_name("username")
        password_field = driver.find_element_by_name("password")
        username_field.send_keys(user_username)
        time.sleep(1)
        password_field.send_keys(user_password)
        time.sleep(1)
        login_button = driver.find_element_by_xpath("/html/body/form/div/button")
        login_button.click()
        time.sleep(2)
        print("Admin has logged in")

        # Admin has logged in
        # Admin clicks View all tickets link to create ticket
        link_create_ticket = driver.find_element_by_link_text('View all tickets')
        time.sleep(1)
        link_create_ticket.click()
        time.sleep(1)
        link_view_ticket = driver.find_element_by_xpath("/html/body/table/tbody/tr[1]/td[3]/a")
        previousRead = driver.find_element_by_xpath("/html/body/table/tbody/tr[1]/td[4]").text
        id = driver.find_element_by_xpath("/html/body/table/tbody/tr[1]/td[1]").text
        time.sleep(1)
        link_view_ticket.click()
        time.sleep(1)
        driver.get("http://127.0.0.1:8000/ticket_creation/display/")
        time.sleep(3)
        newRead = driver.find_element_by_xpath("/html/body/table/tbody/tr[{}]/td[4]".format(id)).text
        self.assertNotEqual(previousRead,newRead)

        driver.quit()
