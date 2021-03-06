import datetime

from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from . import models

from ticket_creation.models import Ticket_Details, All_Tickets
from createuser.models import Extended_User
from input_field_test import Input_field_test
from email_functions import Email_functions
import boto3
from django.db.models import Q

from twilio.rest import Client


account_sid = 'AC4fe51c3cd4fb96c70553e9d6cf9a3a00'
auth_token = '352f733922fb8352dd7e97fcefa279ed'
client = Client(account_sid, auth_token)

error_message_success = "Ticket creation success"
error_message_empty_input = "Please fill in all input fields"
error_message_invalid_input = "Please ensure input fields are valid"
error_message_one_checkbox = "Please choose to be notified via SMS, email, or both"
error_message_unauthorised = "Not authorised"  # used if the token sent by form does not tally with the one specified in /Source/website/input_field_test.py
error_message_forbidden_administrator = "This feature is not available to administrators"
error_message_forbidden_nonadministrator = "This feature is not available to non-administrators"
error_message_email_error = "Error in sending notifications to email"
error_message_unknown_error = "Unknown error"  # thrown when we cant save ticket into model for some reason

highest_queue_number = 5  # (inclusive of the number itself) for iterating tickets along according to queue, a highest queue number is chosen instead of incrementing queue number until there're no more tickets. This is for ease of prototyping (someone might want to make ticket queue number 0 and then queue number 2 during prototyping)
arbitrary_user_for_remote_user = 1  # for remote ticket creation, to be set later when we automate creation of user account when ticket is submitted

no_assigned_admin = "No admin allocated yet"  # used in selected_list, as value of the admin that is assigned to review the ticket


"""
Note:
error_message is still needed for zhijun's tests, so don't remove even if we transmit messages to frontend using Message framework
"""

s3 =boto3.resource('s3', aws_access_key_id='AKIAYWWKI5JM3V7UYB5Y', aws_secret_access_key='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', region_name='ap-southeast-1')

# csrf_exempt so that other websites may access this url without acquiring a csrf token
@csrf_exempt
def create(request):
        """
        Used by nonadmin. If GET request, render template for display. If POST request, checks input validity before creating a new ticket
        """

        name = None  # used in remote creation
        title = None
        email = None  # used in remote creation
        description = None
        phonenumber = None  # used in remote creation
        token = None  # used in remote creation
        is_remote = None  # used in remote creation
        test_pass = False  # state changed when remote/non-remote input passes
        error_message = None

        # user is accessing the ticket_create page explicitly
        if (request.user.is_authenticated):
                # user is logged in
                if not (request.user.is_superuser):
                        # user is normal user
                        if request.method == 'POST':
                                input_field_test = Input_field_test()
                                title = None
                                description = None
                                file = None
                                name = None

                                try:
                                        title = request.POST.get("title")
                                        description = request.POST.get('description')
                                        file = request.FILES.get("file")
                                        if not file:
                                                name = None
                                        else:
                                                name = "https://s3-ap-southeast-1.amazonaws.com/50003/"+file.name
                                                s3.Bucket('50003').put_object(Key=file.name, Body=file)
                                except ValueError:
                                        pass

                                # check input validity
                                title_validity = input_field_test.ticket_title(title)
                                description_validity = input_field_test.ticket_description(description)

                                if len(title_validity)==1 and len(description_validity)==1:
                                        # input is valid
                                        all_tickets = models.All_Tickets(size=0, creator=request.user.id, addressed_by=None, resolved_by=None, read_by=None, queue_number=0, dateTime_created = datetime.datetime.now())
                                        all_tickets.save()

                                        ticket_details = models.Ticket_Details(ticket_id=all_tickets.id, thread_queue_number=0, author=request.user.id, title=title, description=description, image=None, file=name, dateTime_created=datetime.datetime.now())
                                        ticket_details.save()

                                        notify = models.notification(type=0, creater=request.user.get_username(),
                                                                     creater_type=1, ticket_id=all_tickets.id)
                                        notify.save()

                                        messages.add_message(request, messages.SUCCESS, error_message_success)

                                        if Extended_User.objects.get(id=request.user.id).notify_sms == 1:
                                            # if user chose to be notified via sms
                                            print(Extended_User.objects.get(id=request.user.id).phoneNumber)
                                            number = Extended_User.objects.get(id=request.user.id).phoneNumber
                                            try:
                                                message = client.messages \
                                                    .create(
                                                    body="Your ticket " + title + " has been created",
                                                    from_='+12013081881',
                                                    to='+65' + number
                                                )
                                                print(message.sid)
                                            except:
                                                print("invalid number user")



                                        # email notification for all admins (who opted to be notified via email)
                                        nonadmin_username = None
                                        nonadmin_email = None
                                        email_functions = Email_functions()
                                        admin_dict = {}
                                        for i in Extended_User.objects.filter(is_superuser=1, notify_email=1):  # retrieve all admins that want to be notified by email
                                                admin_dict[i.id] = [i.username, i.email]

                                        if Extended_User.objects.get(id=request.user.id).notify_email == 1:  # if nonadmin user wants to be notified through email
                                                nonadmin_username = Extended_User.objects.get(id=request.user.id).username
                                                nonadmin_email = Extended_User.objects.get(id=request.user.id).email

                                        email_status_message = email_functions.ticket_creation_new_ticket(nonadmin_username, nonadmin_email,admin_dict, title, all_tickets.id)
                                        if email_status_message != email_functions.email_sending_success:
                                                error_message = error_message_email_error  #  <-- SUCCESS MESSG HERE
                                        else:
                                                error_message = error_message_success

                                        #for sms notification
                                        for i in Extended_User.objects.filter(is_superuser=1, notify_sms=1):  # retrieve all admins that want to be notified by emai
                                            try:
                                                message = client.messages \
                                                    .create(
                                                    body="A new ticket " + title + " has been created",
                                                    from_='+12013081881',
                                                    to='+65' + str(i.phoneNumber)
                                                )
                                                print(message.sid)

                                            except:
                                                print("invilid phone number")

                                else:
                                        # input fields are not valid
                                        empty_input_state = False
                                        invalid_input_state = False
                                        invalid_token_state = False

                                        for i in title_validity:
                                                if i == "empty":
                                                        empty_input_state = True
                                                elif i == "invalid value":
                                                        invalid_input_state = True
                                        for i in description_validity:
                                                if i == "empty":
                                                        empty_input_state = True
                                                elif i == "invalid value":
                                                        invalid_input_state = True

                                        if invalid_token_state:
                                                # wrong token submitted
                                                error_message = error_message_unauthorised
                                        elif empty_input_state:
                                                # input fields are empty
                                                error_message = error_message_empty_input
                                        elif invalid_input_state:
                                                # input fields have invalid input
                                                error_message = error_message_invalid_input

                                        messages.add_message(request, messages.SUCCESS, error_message)
                                print("@@@@")
                                print(error_message)
                                return render(request, 'createticketform.html', {'error_message':error_message})
                        else:
                                q = models.All_Tickets.objects.filter(queue_number=0)
                                print(q)

                                return render(request, 'createticketform.html', {'error_message':error_message, 'username':request.user.get_username()})
                else:
                        # user is superuser
                        return HttpResponseForbidden()
        else:
                # user is not logged in
                return HttpResponseRedirect(reverse("login:index"))


def list(request):
    """
    Used exclusively by admin to view all available tickets
    """
    if (request.user.is_authenticated):
        # user is logged in
        outputList = []

        if (request.user.is_superuser):
            outputList = sort_ticket_list(request, models.All_Tickets.objects.all(), True)

            return render(request, 'dashboardadmin.html', {"list":outputList})
        else:
            # user is normal user
            return HttpResponseForbidden()

    else:
        return HttpResponseRedirect(reverse("login:index"))

def selected_list(request):
    """
    Used for non-admin and admin users to see a list of tickets they are assigned to/they have submitted
    This is not combined with list() as the admin would have 2 different ways of using this function. Without 
    adding new information to the url that request this, it would be impossible to differentiate when the admin needs one of the two functions
    """
    if (request.user.is_authenticated):
        outputList = []  # list of dictionaries of ticket details

        if (request.user.is_superuser):
            # User is admin
            querySet = models.All_Tickets.objects.filter(addressed_by=request.user.id)
            if querySet != None:
                outputList = sort_ticket_list(request, querySet, request.user.is_superuser)

        else:
            # User is non-admin
            querySet = models.All_Tickets.objects.filter(creator=request.user.id)
            if querySet != None:
                outputList = sort_ticket_list(request, querySet, request.user.is_superuser)

        return render(request, 'viewticketsadmin.html', {"list":outputList, 'view':'My Assigned Tickets'})
    else:
        # user is not authenticated
        return HttpResponseRedirect(reverse("login:index"))


@csrf_exempt
def detail(request):
    """
    Used by admin and nonadmin. If GET request, retrieve data of ticket and its subsequent replies. If POST request,
    submit admin/nonadmin's reply to the ticket, and notify appropriate admin/nonadmin
    """
    error_message = None
    email_notif_pass = False

    if (request.user.is_authenticated):
        # user is loggged in
        ticket_id = request.GET.get("id")  # this works even when submitting replies cos the url is still the same, and "id" is retrieved from the url


        if request.user.is_superuser:
            try:
                remove_notify_ticket = models.notification.objects.get(type=0, ticket_id=ticket_id)
                remove_notify_ticket.delete()
            except:
                remove_notify_ticket = None
        try:
            remove_notify_msg = models.notification.objects.filter(ticket_id=ticket_id)
            remove_notify_msg = remove_notify_msg.filter(~Q(creater=request.user.get_username()))
            remove_notify_msg.delete()
        except:
            remove_notify_msg = None

        if request.method == "POST":
            # user is posting reply to ticket
            input_field_test = Input_field_test()
            description = None
            all_tickets_row = None
            name = None
            file = None

            try:
                description = request.POST.get("description")
                file = request.FILES.get("file")

                if not file:
                    name = None
                    print("Nonefile")
                else:
                    name = "https://s3-ap-southeast-1.amazonaws.com/50003/" + file.name
                    s3.Bucket('50003').put_object(Key=file.name, Body=file)

            except ValueError:
                pass

            description_validity = input_field_test.ticket_description(description)

            if len(description_validity)==1:
                # update data of thread under All_Tickets
                all_tickets_row = models.All_Tickets.objects.get(id=ticket_id)
                new_queue_number = all_tickets_row.size + 1
                all_tickets_row.size = new_queue_number
                all_tickets_row.save()



                # creation of new entry into Ticket_Detail
                ticket_details_row = models.Ticket_Details(ticket_id=ticket_id, thread_queue_number=new_queue_number, author=request.user.id, description=description, image=None, file=name, dateTime_created=datetime.datetime.now())
                ticket_details_row.save()

                #create msg notification
                creater_type = None
                if request.user.is_superuser:
                    creater_type=0
                else:
                    creater_type=1
                notify = models.notification(type=1, creater=request.user.get_username(), creater_type=creater_type,
                                             ticket_id=ticket_id)
                notify.save()

                # updating read_by attribute of All_Ticket to be only read by the user posting the reply
                # updating addressed by to the first admin that replies if addressed_by==None
                all_tickets_row.read_by = str(request.user.id)+","
                if (request.user.is_superuser):
                    addressed_by = all_tickets_row.addressed_by
                    if addressed_by == None:
                        all_tickets_row.addressed_by = request.user.id
                        all_tickets_row.save()



                # email notification for ticket replying
                if (request.user.is_superuser):
                    # if admin made a reply - notify nonadmin
                    nonadmin_username = None
                    nonadmin_email = None
                    nonadmin_id = all_tickets_row.creator
                    ticket_id = all_tickets_row.id
                    ticket_title = Ticket_Details.objects.get(ticket_id=ticket_id, thread_queue_number=0).title
                    email_functions = Email_functions()

                    if Extended_User.objects.get(id=nonadmin_id).notify_email==1:
                        nonadmin_username = Extended_User.objects.get(id=nonadmin_id).username
                        nonadmin_email = Extended_User.objects.get(id=nonadmin_id).email

                    email_notif_response = email_functions.ticket_creation_admin_replies(nonadmin_username, nonadmin_email, ticket_title, ticket_id)
                    if email_notif_response == email_functions.email_sending_success:
                        email_notif_pass = True

                else:
                    # if nonadmin made a reply - notify assigned admin/all admin
                    assigned_admin_id = all_tickets_row.addressed_by
                    assigned_admin_username = None
                    assigned_admin_email = None
                    admin_dict = {}
                    email_functions = Email_functions()
                    ticket_id = all_tickets_row.id
                    ticket_title = Ticket_Details.objects.get(ticket_id=ticket_id, thread_queue_number=0).title

                    if assigned_admin_id != None:
                        if Extended_User.objects.get(id=assigned_admin_id).notify_email==1:
                            # when there is an admin assigned to the ticket, and admin wants to be notified by email
                            assigned_admin_username = Extended_User.objects.get(id=assigned_admin_id).username
                            assigned_admin_email = Extended_User.objects.get(id=assigned_admin_id).email

                    for i in Extended_User.objects.filter(is_superuser=1, notify_email=1):
                        admin_dict[i.id] = [i.username, i.email]

                    email_notif_response = email_functions.ticket_creation_nonadmin_replies(assigned_admin_username, assigned_admin_email, admin_dict, ticket_title, ticket_id)
                    if email_notif_response == email_functions.email_sending_success:
                        email_notif_pass = True


                if email_notif_pass:
                    messages.add_message(request, messages.SUCCESS, error_message_success)
                    error_message = error_message_success
                else:
                    messages.add_message(request, messages.ERROR, error_message_email_error)
                    error_message = error_message_email_error

                # sms notification
                if (request.user.is_superuser):
                    nonadmin_username = None
                    nonadmin_phone = None
                    # if admin made a reply - notify nonadmin
                    nonadmin_id = all_tickets_row.creator
                    ticket_id = all_tickets_row.id
                    ticket_title = Ticket_Details.objects.get(ticket_id=ticket_id, thread_queue_number=0).title

                    if Extended_User.objects.get(id=nonadmin_id).notify_sms==1:
                        nonadmin_username = Extended_User.objects.get(id=nonadmin_id).username
                        nonadmin_phone = Extended_User.objects.get(id=nonadmin_id).phoneNumber
                        try:
                            message = client.messages \
                                .create(
                                body="You have receive a reply regarding to your ticket " + ticket_title + " from Accenture",
                                from_='+12013081881',
                                to='+65' + nonadmin_phone
                            )

                            print(message.sid)
                        except:
                            print("invilid number")


                else:
                    # if nonadmin made a reply - notify assigned admin/all admin
                    assigned_admin_id = all_tickets_row.addressed_by
                    assigned_admin_username = None
                    assigned_admin_phone = None
                    admin_dict = {}
                    ticket_id = all_tickets_row.id
                    ticket_title = Ticket_Details.objects.get(ticket_id=ticket_id, thread_queue_number=0).title

                    if assigned_admin_id != None:
                        if Extended_User.objects.get(id=assigned_admin_id).notify_email==1:
                            # when there is an admin assigned to the ticket, and admin wants to be notified by email
                            assigned_admin_username = Extended_User.objects.get(id=assigned_admin_id).username
                            assigned_admin_phone = Extended_User.objects.get(id=assigned_admin_id).phoneNumber

                            try:
                                message = client.messages \
                                    .create(
                                    body="A new reply regarding to " + ticket_title + " has received from user",
                                    from_='+12013081881',
                                    to='+65' + assigned_admin_phone
                                )

                                print(message.sid)
                            except:
                                print("invilid number")

                    else:
                        for i in Extended_User.objects.filter(is_superuser=1, notify_sms=1):
                            print(i.phoneNumber)
                            try:
                                message = client.messages \
                                    .create(
                                    body="A new reply regarding to " + ticket_title + " has received from user",
                                    from_='+12013081881',
                                    to='+65' + i.phoneNumber
                                )

                                print(message.sid)
                            except:
                                print("wrong phone number")

            else:
                # input fields are not valid
                empty_input_state = False
                invalid_input_state = False
                invalid_token_state = False

                for i in description_validity:
                    if i == "empty":
                        empty_input_state = True
                    elif i == "invalid value":
                        invalid_input_state = True

                if invalid_token_state:
                    # wrong token submitted
                    error_message = error_message_unauthorised
                elif empty_input_state:
                    # input fields are empty
                    error_message = error_message_empty_input
                elif invalid_input_state:
                    # input fields have invalid input
                    error_message = error_message_invalid_input

                messages.add_message(request, messages.SUCCESS, error_message)

            return HttpResponseRedirect(reverse("ticket_creation:detail")+"?id={0}".format(ticket_id))

        else:
            # user is retrieving the message thread of a ticket
            outputList = []
            all_tickets_data = {}
            all_tickets_row = models.All_Tickets.objects.get(id=ticket_id)


            # Check if user is authorised to this feature - User can only view the ticket if (1. User is admin) (2. User is non-admin and author of ticket)
            is_admin = request.user.is_superuser
            is_author = request.user.id == all_tickets_row.creator
            is_authorised = is_admin or (not is_admin and is_author)

            if is_authorised:  # prevent non-admin users from accessing/replying to tickets that they didnt write
                info = models.Ticket_Details.objects.get(ticket_id=ticket_id, thread_queue_number=0)

                for i in range(all_tickets_row.size + 1):  # note that index=0 and index=size both represents some ticket/reply
                    ticketDetails = {"username": None, "user": None, "description": None, "time": None, "type": None,
                                     "file": None}
                    ticket_details_row = models.Ticket_Details.objects.get(ticket_id=ticket_id, thread_queue_number=i)
                    ticketDetails["id"] = ticket_details_row.id  # id of this ticket/reply (in Ticket_Details)
                    ticketDetails["user"] = ticket_details_row.author  # author of this particular ticket/reply
                    ticketDetails["description"] = ticket_details_row.description
                    ticketDetails["ticket_id"] = ticket_details_row.ticket_id  # id of the ticket that this ticket/reply (in All_Ticket) is tied to
                    ticketDetails["file"] = ticket_details_row.file

                    ticketDetails["time"] = ticket_details_row.dateTime_created
                    ticketDetails["username"] = Extended_User.objects.get(id=ticket_details_row.author).username
                    if ticketDetails["user"] == request.user.id:
                        ticketDetails["type"] = 0
                    else:
                        ticketDetails["type"] = 1
                    outputList.append(ticketDetails)

                # updating read_by attribute of All_Ticket to include the current user
                read_by = all_tickets_row.read_by
                if read_by == None:
                    all_tickets_row.read_by = str(request.user.id)+","
                else:
                    if str(request.user.id) in all_tickets_row.read_by.split(","):
                        pass
                    else:
                        all_tickets_row.read_by += str(request.user.id)+","
                all_tickets_row.save()

                # fill up all_tickets_data
                all_tickets_data["resolved_by"] = all_tickets_row.resolved_by

                if request.user.is_superuser:
                    return render(request, 'detail.html', {"info":info, "item": outputList, "all_tickets_data":all_tickets_data,'username':request.user.get_username()})
                else:

                    return render(request, 'detail_user.html', {"info":info,"item": outputList, "all_tickets_data":all_tickets_data,'username':request.user.get_username()})
            else:
                print("hihi")
                return HttpResponseForbidden()

    else:
        # user is not logged in
        return HttpResponseRedirect(reverse("login:index"))



def delete(request):
        """
        Used by admin. Deletes ticket permenantly.
        """
        if (request.user.is_authenticated):
                # user is logged in
                if (request.user.is_superuser):
                        # user is superuser
                        column_id = request.GET.get("id")
                        models.All_Tickets.objects.filter(id=column_id).delete()
                        models.Ticket_Details.objects.filter(ticket_id=column_id).delete()

                        return HttpResponseRedirect(reverse("home:index"))
                else:
                        # user is normal user
                        return HttpResponseRedirect(reverse("home:index"))
        else:
                # user is not logged in
                return HttpResponseRedirect(reverse("login:index"))

def resolve(request):
    """
    Used by admin. Mark tickets as resolved
    """

    if (request.user.is_authenticated):
        # user is logged in
        if (request.user.is_superuser):
            column_id = request.GET.get("id")
            models.All_Tickets.objects.filter(id=column_id).update(resolved_by=request.user.id)

            notification = models.notification(type=0, creater=request.user.get_username(),creater_type=0, ticket_id=column_id)
            notification.save()

            nonadmin_id = models.All_Tickets.objects.get(id=column_id).creator
            ticket_id = column_id
            ticket_title = Ticket_Details.objects.get(ticket_id=column_id, thread_queue_number=0).title

            if Extended_User.objects.get(id=nonadmin_id).notify_sms == 1:
                nonadmin_username = Extended_User.objects.get(id=nonadmin_id).username
                nonadmin_phone = Extended_User.objects.get(id=nonadmin_id).phoneNumber
                print(nonadmin_phone)

                message = client.messages \
                    .create(
                    body="Your ticket " + ticket_title + " has been resolved by Accenture",
                    from_='+12013081881',
                    to='+65' + nonadmin_phone
                )

                print(message.sid)


            return HttpResponseRedirect(reverse("home:index"))
        else:
            # user is normal user - note that only admin users can resolve tickets
            return HttpResponseForbidden()
    else:
        return HttpResponseRedirect(reverse("login:index"))

def sort_ticket_list(request, querySetObj, is_superuser):
    """
    Private function used by list() and selected_list()

    Takes a list of QuerySet objects (specifically elements in the Ticket_Details table), sorts through accordingly and
    outputs ordered list of ticket details

    Order:
    All unread tickets
        unresolved tickets
            according to priority queue
        resolved tickets
            according to priority queue
    All read tickets
        unresolved tickets
            according to priority queue
        resolved tickets
            according to priority queue

    """
    outputList = []
    readList = [[],[]]  # unresolved tickets, resolved tickets
    nonreadList = [[],[]]  # unresolved tickets, resolved tickets

    for i in range(highest_queue_number+1):
        for j in querySetObj.filter(queue_number=i):
            if j.id != None:
                read_state = False
                resolve_state = False

                if j.read_by != None:
                    if str(request.user.id) in j.read_by.split(","):
                        read_state = True
                    else:
                        read_state = False
                else:
                    read_state = False

                if j.resolved_by != None:
                    resolve_state = True
                else:
                    resolve_state = False

                if read_state and not resolve_state:
                    readList[0].append(j)
                elif read_state and resolve_state:
                    readList[1].append(j)
                elif not read_state and not resolve_state:
                    nonreadList[0].append(j)
                elif not read_state and resolve_state:
                    nonreadList[1].append(j)

    for i in nonreadList,readList:  # first nonreadList, then readList
        for j in i:  # first unresolved tickets, then resolved tickets
            for k in j:  # for all elements in unresolved/resolved tickets
                each_ticket = {"id":None, "user":None, "title":None, "read":None, "resolved":None, "read_by":None}
                each_ticket["id"] = k.id

                if (request.user.is_superuser):
                    each_ticket["user"] = Extended_User.objects.get(id=k.creator)  # in the perspective of the admin, this will display author of ticket
                else:
                    if k.resolved_by != None:
                        each_ticket["user"] = Extended_User.objects.get(id=k.resolved_by)  # in the perspective of the user, this will display the name of the admin addressing the issue
                    else:
                        each_ticket["user"] = no_assigned_admin

                each_ticket["title"] = models.Ticket_Details.objects.get(ticket_id=k.id, thread_queue_number=0).title

                if k.read_by != None:
                    each_ticket["read"] = str(request.user.id) in k.read_by.split(",")
                else:
                    each_ticket["read"] = False

                if k.resolved_by == None:
                    each_ticket["resolved"] = False
                else:
                    each_ticket["resolved"] = True

                each_ticket["read_by"] = k.read_by
                outputList.append(each_ticket)

    return outputList

def viewUnread(request):
    """
    Used by admin. Views all unread tickets by admin.
    """

    if (request.user.is_authenticated):
        if (request.user.is_superuser):
            list = []
            all_tickets = sort_ticket_list(request, models.All_Tickets.objects.all(), request.user.is_superuser)

            for i in all_tickets:
                if i["read_by"] == None:
                    list.append(i)
                elif str(request.user.id) not in i["read_by"]:
                    list.append(i)

            return render(request, 'viewticketsadmin.html',{'list':list, 'view':'All Unread Tickets'})
        else:
            return HttpResponseRedirect(reverse("home:index"))
    else:
        return HttpResponseRedirect(reverse("login:index"))

def viewUnresolved(request):
    """
    Used by admin. Views all unresolved tickets by admin
    """

    if (request.user.is_authenticated):
        if (request.user.is_superuser):
            list = sort_ticket_list(request, models.All_Tickets.objects.all().filter(resolved_by=None), request.user.is_superuser)

            return render(request, 'viewticketsadmin.html',{'list':list, 'view':'All Unresolved Tickets'})
        else:
            return HttpResponseRedirect(reverse("home:index"))
    else:
        return HttpResponseRedirect(reverse("login:index"))
