from django.shortcuts import render
from django.core.mail import send_mail
from django.core.mail import mail_admins
from django.conf import settings
from createuser.models import Extended_User
import requests  # to access acnapi
import smtplib
import copy

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def email_to_admin(request): # seems like this one works
	subject = 'New ticket incoming'
	message = 'You have a new support request'
	email_from = 'pleasedontlockthisemailthanks@gmail.com'
	email_to = 'john@example.com' # admin email hardcoded

	msg = MIMEMultipart()
	msg['From'] = email_from
	msg['To'] = email_to
	msg['Subject'] = subject
	body = message
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP('smtp.gmail.com', 25)
	server.connect('smtp.gmail.com', 25)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('pleasedontlockthisemailthanks@gmail.com', "e@5yp@55w0rd")
	text = msg.as_string()
	server.sendmail(email_from, email_to, text)
	server.quit()


def email_from_admin(request):
	subject = 'ADMIN replied to your request'
	message = 'View comment by admin'
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [] #need to do something about this
	send_mail(subject, message, email_from, recipient_list,fail_silently=False)

def email_to_user(request):
	subject = 'Your ticket has been created'
	message = 'Awaiting admin help'
	email_from = 'pleasedontlockthisemailthanks@gmail.com'
	email_to = request.POST.get('email')

	msg = MIMEMultipart()
	msg['From'] = email_from
	msg['To'] = email_to
	msg['Subject'] = subject
	body = message
	msg.attach(MIMEText(body,'plain'))
	server = smtplib.SMTP('smtp.gmail.com',25)
	server.connect('smtp.gmail.com',25)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('pleasedontlockthisemailthanks@gmail.com',"e@5yp@55w0rd")
	text = msg.as_string()
	server.sendmail(email_from,email_to,text)
	server.quit()




def acnapi_email(email_subject, email_recipient, email_html):
        """
        Private method, sends email to destination through support@accenture.com
        """
        url = "https://ug-api.acnapiv3.io/swivel/email-services/api/mailer"
        payload = {"subject":None, "sender":"support@accenture.com", "recipient":None, "html":None}
        headers = {"Host":"ug-api.acnapiv3.io", "Server-Token":None, "Content-Type":"application/json", "cache-control":"no-cache",  $
        token_file_contents = None
        counter0 = 2  # a counter that counts the number of values we need to retrieve from tokens.txt

        with open("tokens.txt") as token_file:
                token_file_contents = copy.deepcopy(token_file.readlines())

        for i in token_file_contents:
                if "Server-Token" in i:
                        headers["Server-Token"] = i.split(":")[1][:-1]  # slice the string to remove "/n" char
                        counter0 -= 1
                elif "Postman-Token" in i:
                        headers["Postman-Token"] = i.split(":")[1][:-1]  # slice the string to remove "/n char"
                        counter0 -= 1

        # check if all necessary values are retrieved
        if counter0 != 0:
                print("tokens.txt do not have the values acnapi_email() is looking for")
                return

        payload["subject"] = email_subject
        payload["recipient"] = email_recipient
        payload["html"] = email_html

        response = requests.post(url, json=payload, headers=headers)
        print(response.status_code==200)

