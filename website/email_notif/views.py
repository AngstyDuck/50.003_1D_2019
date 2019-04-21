from django.shortcuts import render
from django.core.mail import send_mail
from django.core.mail import mail_admins
from django.conf import settings
from createuser.models import Extended_User
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Create your views here.


# def email_to_admin(request): # seems like this one works (kinda wonk)
#     subject = 'New ticket incoming'
#     message = 'You have a new support request'
#     # email_from = settings.EMAIL_HOST_USER
#     mail_admins(subject, message,fail_silently=False)

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

    #send_mail(subject, message, email_from, recipient_list,fail_silently=False)



#def admin_emails(request):
#    return {'ADMINS': settings.ADMINS}
