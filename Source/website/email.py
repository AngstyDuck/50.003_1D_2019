from createuser.models import Extended_User
from ticket_creation.models import All_Tickets

import requests
import copy

email_sending_success = "Email is sent successfully"
email_sending_error = "Error faced when sending email"




def acnapi_email(email_recipient, email_subject, email_html):
	"""
	Private method, sends email to destination through support@accenture.com
	"""
	url = "https://ug-api.acnapiv3.io/swivel/email-services/api/mailer"
	payload = {"subject":None, "sender":"support@accenture.com", "recipient":None, "html":None}
	headers = {"Host":"ug-api.acnapiv3.io", "Server-Token":None, "Content-Type":"application/json", "cache-control":"no-cache", "$
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


def retrieve_all_admin_email():
	"""
	Private method, returns dictionary of admin username (as key) and admin email (as value)

	Uses the inherent attribute "is_staff" of the createuser_extended_user mysql table
	"""
	output = {}
	all_admin = Extended_User.object.filter(is_staff=1)

	for admin in all_admin:
		output[admin.username] = admin.email

	print("@@@@retrieve_all_admin_email test")
	print(output)
	return output


def index(email_type, ticket_id):
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
		nonadmin_id = All_Tickets.objects.get(id=ticket_id).get("creator")
		nonadmin_username = Extended_User.objects.get(id=nonadmin_id).get("username")
		nonadmin_email = Extended_User.objects.get(id=nonadmin_id).get("email")
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
		admin_id = All_Tickets.objects.get(id=ticket_id).get("addressed_by")

		if admin_id == None:
			# no admin assigned to ticket yet - email is sent to all admin to tell them that nonadmin has replied to ticket
			admin_email = retrieve_all_admin_email()

			for i in admin_email.keys():
				message = "{0}, ".format(i) + 'you have a new support request'  # for dat personalization ;))))
				if acnapi_email(admin_email[i], subject, message) == email_sending_error:
					return email_sending_error
			return email_sending_success

		else:
			# admin has been assigned to the ticket
			pass


	elif email_type == 3:
		pass
	elif email_type == 4:
		pass

