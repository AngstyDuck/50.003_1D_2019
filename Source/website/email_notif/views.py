from django.shortcuts import render
from django.conf import settings
from createuser.models import Extended_User
import requests  # to access acnapi
import copy


email_sending_success = "Email is sent successfully"
email_sending_error = "Error faced when sending email"


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


def index(request, email_type):
	"""
	Public method. All requests to send email will lead to this url. email_type represents an integer that describes 
	the circumstance that this url may be called. The text in the email is hardcoded here in accordance to the circumstance.

	Different email_type:
	1 - When non-admin submits new ticket (email sent to non-admin himself, and all admins)
	2 - When non-admin replies to existing ticket (email sent to admin assigned to it (or all admins if no admins is assigned))
	3 - When admin replies to existing ticket (email sent to author of ticket (non-admin))
	3 - When non-admin resets password (email sent to all admins)
	"""
	if email_type == 1:
		nonadmin_username = Extended_User.objects.get("id"=request.user.id).username
		nonadmin_email = Extended_User.objects.get("id"=request.user.id).email
		all_admin_email = retrieve_all_admin_email()

		# for non-admin
		subject = 'Your ticket has been created'
		message = "{0}, ".format(nonadmin_username) + 'your ticket is awaiting admin help'  # for dat personalization ;))))
		if acnapi_email(nonadmin_email, subject, message) == email_sending_error:
			return email_sending_error

		# for all admin
		subject = 'New ticket incoming'
		for i in all_admin_email.keys():
			message = "{0}, ".format(i) + 'you have a new support request'  # for dat personalization ;))))
			if acnapi_email(all_admin_email[i], subject, message) == email_sending_error:
				return email_sending_error

		return email_sending_success

	elif email_type == 2:
		pass
	elif email_type == 3:
		pass
	elif email_type == 4:
		pass





def retrieve_all_admin_email():
	"""
	Private method, returns dictionary of admin username (as key) and admin email (as value)

	Uses the inherent attribute "is_staff" of the createuser_extended_user mysql table
	"""
	output = {}
	all_admin = Extended_User.object.filter("is_staff"=1)

	for admin in all_admin:
		output[admin.username] = admin.email

	print("@@@@retrieve_all_admin_email test")
	print(output)
	return output



def acnapi_email(email_recipient, email_subject, email_html):
	"""
	Private method, sends email to destination through support@accenture.com
	"""
	url = "https://ug-api.acnapiv3.io/swivel/email-services/api/mailer"
	payload = {"subject":None, "sender":"support@accenture.com", "recipient":None, "html":None}
	headers = {"Host":"ug-api.acnapiv3.io", "Server-Token":None, "Content-Type":"application/json", "cache-control":"no-cache", "Postman-Token":None}
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

	if response.status_code == 200:
		return email_sending_success
	else:
		return email_sending_error
