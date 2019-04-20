import datetime

from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse

from . import models
from createuser.models import Extended_User

from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from email_notif.views import email_from_admin
from email_notif.views import email_to_admin
from email_notif.views import email_to_user

from createuser.models import Extended_User
from input_field_test import Input_field_test
import boto3

error_message_success = "Ticket creation success"
error_message_empty_input = "Please fill in all input fields"
error_message_invalid_input = "Please ensure input fields are valid"
error_message_one_checkbox = "Please choose to be notified via SMS, email, or both"
error_message_unauthorised = "Not authorised"  # used if the token sent by form does not tally with the one specified in /Source/website/input_field_test.py
error_message_forbidden_administrator = "This feature is not available to administrators"
error_message_forbidden_nonadministrator = "This feature is not available to non-administrators"
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
        Other than accessing the ticket_creation page, this view is to be accessed by remote form (/TestForm/forms/views.py).. Checking of input validity will only be done here,
        not in the form.

        Prepared to receive the following key-values:
        title - title of ticket
        description - description of ticket
        name - Only alphabets
        phonenumber - Only integers
        email - Only alphabets, integers, one '@', and multiple '.'
        token - Any characters, used to validate that the one accessing our url is our forms (specificed in TestForm/forms/views.py and /Source/website/input_field_test.py)

        When input is valid, sends error_message as HttpResponse to form (even if input is valid). Possible error_messages include
        errro_message_success, errro_message_empty_input, errro_message_invalid_input, errro_message_unauthorised, error_message_unknown_error

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

        # checking if this url is the posting of remote form
        if request.method == 'POST':
                try:
                        is_remote = request.POST.get('is_remote')
                except ValueError:
                        pass

        # remote connet to this url
        if is_remote == "True":
                try:
                        name = request.POST.get("name")
                        title = request.POST.get("title")
                        email = request.POST.get('email')
                        phonenumber = request.POST.get('phonenumber')
                        description = request.POST.get('description')
                        token = request.POST.get('token')
                except ValueError:
                        pass

                input_field_test = Input_field_test()
                username_validity = input_field_test.username(name)
                title_validity = input_field_test.ticket_title(title)
                email_validity = input_field_test.email(email)
                description_validity = input_field_test.ticket_description(description)
                phonenumber_validity = input_field_test.phonenumber(phonenumber)
                token_validity = input_field_test.token(token)

                if (len(username_validity)==1 and len(title_validity)==1 and len(email_validity)==1 and len(description_validity)==1 and len(phonenumber_validity)==1 and len(token_validity)==1):
                        try:
                                all_tickets = models.All_Tickets(size=0, creator=arbitrary_user_for_remote_user, addressed_by=None, resolved_by=None, read_by=None, queue_number=0, dateTime_created = datetime.datetime.now())
                                all_tickets.save()

                                ticket_details = models.Ticket_Details(ticket_id=all_tickets.id, thread_queue_number=0, author=0, title=title, description=description, image=None, file=None, dateTime_created=datetime.datetime.now())
                                ticket_details.save()
                                error_message = error_message_success
                        except Exception:
                                error_message = error_message_unknown_error
                else:
                        # input fields are not valid
                        empty_input_state = False
                        invalid_input_state = False
                        invalid_token_state = False

                        for i in username_validity:
                                if i == "empty":
                                        empty_input_state = True
                                elif i == "invalid value":
                                        invalid_input_state = True
                        for i in title_validity:
                                if i == "empty":
                                        empty_input_state = True
                                elif i == "invalid value":
                                        invalid_input_state = True
                        for i in email_validity:
                                if i == "empty":
                                        empty_input_state = True
                                elif i == "invalid value":
                                        invalid_input_state = True
                        for i in description_validity:
                                if i == "empty":
                                        empty_input_state = True
                                elif i == "invalid value":
                                        invalid_input_state = True
                        for i in phonenumber_validity:
                                if i == "empty":
                                        empty_input_state = True
                                elif i == "invalid value":
                                        invalid_input_state = True
                        for i in token_validity:
                                if i == "invalid value":
                                        invalid_token_state = True

                        if invalid_token_state:
                                # wrong token submitted
                                error_message = error_message_unauthorised
                        elif empty_input_state:
                                # input fields are empty
                                error_message = error_message_empty_input
                        elif invalid_input_state:
                                # input fields have invalid input
                                error_message = error_message_invalid_input

                return HttpResponse(error_message)

        # user is accessing the ticket_create page explicitly
        elif (request.user.is_authenticated):
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
                                        file = request.FILES.get('file')
                                        if not file:
                                            name=None
                                        else:
                                            name = "https://s3-ap-southeast-1.amazonaws.com/50003/"+file.name
                                            s3.Bucket('50003').put_object(Key=file.name, Body=file)
                                except ValueError:
                                        pass

                                title_validity = input_field_test.ticket_title(title)
                                description_validity = input_field_test.ticket_description(description)

                                if len(title_validity)==1 and len(description_validity)==1:

                                        all_tickets = models.All_Tickets(size=0, creator=request.user.id, addressed_by=None, resolved_by=None, read_by=None, queue_number=0, dateTime_created = datetime.datetime.now())
                                        all_tickets.save()

                                        ticket_details = models.Ticket_Details(ticket_id=all_tickets.id,
                                                                               thread_queue_number=0,
                                                                               author=request.user.id, title=title,
                                                                               description=description, image=None,
                                                                               file=name,
                                                                               dateTime_created=datetime.datetime.now())
                                        ticket_details.save()
                                        messages.add_message(request, messages.SUCCESS, error_message_success)
                                        error_message = error_message_success

                                        email_to_admin(request) # uses mail_admins
                                        # email_to_user(request) # uses send_mail
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
                                send_mail('Ticket Created Successful','Your ticket '+title+' has been create successful','50003escproject@gmail.com',[request.user.email],fail_silently=False)
                                return render(request, 'createticketform.html', {'error_message':error_message} )
                        else:
                                q = models.All_Tickets.objects.filter(queue_number=0)
                                print(q)

                                return render(request, 'createticketform.html', {'username':request.user.get_username()})
                else:
                        # user is superuser
                        return HttpResponseForbidden(error_message_forbidden_administrator)
        else:
                return HttpResponseRedirect(reverse("login:index"))


def list(request):
    """
    Used exclusively by admin to view all available tickets
    """
    if (request.user.is_authenticated):
        # user is logged in
        outputList = []

        if (request.user.is_superuser):
            outputList = sort_ticket_list(request, models.All_Tickets.objects.all(), request.user.is_superuser)

            return render(request, 'viewticketsadmin.html', {"list":outputList})
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

        return render(request, 'ticketcreation/show.html', {"list":outputList})
    else:
        # user is not authenticated
        return HttpResponseRedirect(reverse("login:index"))

def detail(request):
    error_message = None
    if (request.user.is_authenticated):
        # user is loggged in
        ticket_id = request.GET.get("id")  # this works even when submitting replies cos the url is still the same, and "id" is retrieved from the url

        if request.method == "POST":
            # user is posting reply to ticket
            input_field_test = Input_field_test()
            title = None
            description = None
            all_tickets_row = None


            try:
                title = request.POST.get("title")
                description = request.POST.get("description")
            except ValueError:
                pass

            title_validity = input_field_test.ticket_title(title)
            description_validity = input_field_test.ticket_description(description)

            if len(title_validity)==1 and len(description_validity)==1:
                # update data of thread under All_Tickets
                all_tickets_row = models.All_Tickets.objects.get(id=ticket_id)
                new_queue_number = all_tickets_row.size + 1
                all_tickets_row.size = new_queue_number
                all_tickets_row.save()

                # creation of new entry into Ticket_Detail
                ticket_details_row = models.Ticket_Details(ticket_id=ticket_id, thread_queue_number=new_queue_number, author=request.user.id, title=title, description=description, image=None, file=None, dateTime_created=datetime.datetime.now())
                ticket_details_row.save()

                # updating read_by attribute of All_Ticket to be only read by the user posting the reply
                # updating addressed by to the first admin that replies if addressed_by==None
                all_tickets_row.read_by = str(request.user.id)+","
                if (request.user.is_superuser):
                    addressed_by = all_tickets_row.addressed_by
                    if addressed_by == None:
                        all_tickets_row.addressed_by = request.user.id
                        all_tickets_row.save()

                messages.add_message(request, messages.SUCCESS, error_message_success)
                error_message = error_message_success
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

            return HttpResponseRedirect(reverse("ticket_creation:detail")+"?id={0}".format(ticket_id))

        else:
            # user is retrieving the message thread of a ticket
            # ----- instantiate and declare variables
            outputList = []
            all_tickets_data = {}

            # ----- retrival of data
            all_tickets_row = models.All_Tickets.objects.get(id=ticket_id)

            for i in range(all_tickets_row.size+1):   # note that index=0 and index=size both represents some ticket/reply
                ticketDetails = {"title":None, "id":None, "user":None, "description":None, "ticket_id":None,'file':None}
                ticket_details_row = models.Ticket_Details.objects.get(ticket_id=ticket_id, thread_queue_number=i)

                ticketDetails["title"] = ticket_details_row.title
                ticketDetails["id"] = ticket_details_row.id  # id of this ticket/reply (in Ticket_Details)
                ticketDetails["user"] = ticket_details_row.author  # author of this particular ticket/reply
                ticketDetails["description"] = ticket_details_row.description
                ticketDetails["ticket_id"] = ticket_details_row.ticket_id  # id of the ticket that this ticket/reply (in All_Ticket) is tied to
                ticketDetails['file']=ticket_details_row.file
                outputList.append(ticketDetails)

            # updating read_by attribute of All_Ticket to include the current user
            read_by = all_tickets_row.read_by
            if read_by == None:
                all_tickets_row.read_by = str(request.user.id)+","
            else:
                if request.user.id in all_tickets_row.read_by.split(","):
                    pass
                else:
                    all_tickets_row.read_by += str(request.user.id)+","
            all_tickets_row.save()

            # fill up all_tickets_data
            all_tickets_data["resolved_by"] = all_tickets_row.resolved_by
            if request.user.is_superuser:
                return render(request, 'detail.html', {"item": outputList, "all_tickets_data":all_tickets_data,'username':request.user.get_username()})
            else:
                return render(request, 'detail_user.html', {"item": outputList, "all_tickets_data":all_tickets_data,'username':request.user.get_username()})
    else:
        return HttpResponseRedirect(reverse("login:index"))

def delete(request):
        if (request.user.is_authenticated):
            # user is logged in
            if (request.user.is_superuser):
                # user is superuser
                column_id = request.GET.get("id")
                models.All_Tickets.objects.filter(id=column_id).delete()
                models.Ticket_Details.objects.filter(ticket_id=column_id).delete()

                return HttpResponseRedirect(reverse("ticket_creation:display"))
            else:
                # user is normal user
                return HttpResponseRedirect(reverse("home:index"))
        else:
            # user is not logged in
            return HttpResponseRedirect(reverse("login:index"))


def resolve(request):
    print("PING")
    if (request.user.is_authenticated):
        # user is logged in
        if (request.user.is_superuser):
            column_id = request.GET.get("id")
            print(column_id)
            models.All_Tickets.objects.filter(id=column_id).update(resolved_by=request.user.id)

            return HttpResponseRedirect(reverse("home:index"))
        # return render(request, 'ticketcreation/show.html', {"list": list})
        else:
            # user is normal user
            return HttpResponseRedirect(reverse("home:index"))
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
                each_ticket = {"id":None, "user":None, "title":None, "read":None, "resolved":None}
                each_ticket["id"] = k.id

                if (is_superuser):
                    if k.resolved_by != None:
                        each_ticket["user"] = Extended_User.objects.get(id=k.creator)  # in the perspective of the admin, this will display author of ticket
                    else:
                        each_ticket["user"] = no_assigned_admin
                else:
                    if k.resolved_by != None:
                        each_ticket["user"] = Extended_User.objects.get(id=k.resolved_by)  # in the perspective of the user, this will display the name of the admin addressing the issue
                    else:
                        each_ticket["user"] = no_assigned_admin

                try:
                    each_ticket["title"] = models.Ticket_Details.objects.get(ticket_id=k.id, thread_queue_number=0).title
                except:
                    print("wrong value")

                if k.read_by != None:
                    each_ticket["read"] = str(request.user.id) in k.read_by.split(",")
                else:
                    each_ticket["read"] = False

                if k.resolved_by == None:
                    each_ticket["resolved"] = False
                else:
                    each_ticket["resolved"] = True

                outputList.append(each_ticket)

    return outputList


def viewUnread(request):
    if (request.user.is_authenticated):
        if (request.user.is_superuser):
            list = sort_ticket_list(request,models.All_Tickets.objects.all().filter(read_by=None),request.user.is_superuser)
            return render(request, 'viewticketsadmin.html',{'list':list})
        else:
            return HttpResponseRedirect(reverse("home:index"))
    else:
        return HttpResponseRedirect(reverse("login:index"))

def viewUnresolved(request):
    if (request.user.is_authenticated):
        if (request.user.is_superuser):
            list = sort_ticket_list(request, models.All_Tickets.objects.all().filter(resolved_by=None), request.user.is_superuser)

            return render(request, 'viewticketsadmin.html',{'list':list})
        else:
            return HttpResponseRedirect(reverse("home:index"))
    else:
        return HttpResponseRedirect(reverse("login:index"))
