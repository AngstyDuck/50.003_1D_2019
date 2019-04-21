from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from createuser.models import Extended_User as User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .forms import UserForm
from django.contrib import messages
from input_field_test import Input_field_test


error_message_user_exist = "User already exist"
error_message_empty_input = "Please fill in all input fields"
error_message_invalid_input = "Please ensure input fields are valid"

@csrf_exempt
def get_user(request):
	error_message = None
	#messages.add_message(request, messages.ERROR, 'User Exist!')
	if request.method == 'POST':
                # all variables declared here
                username_validity = []
                password_validity = []
                email_validity = []
                phonenumber_validity = []
                username = None
                password = None
                email = None
                phonenumber = None

                try:
                        username = request.POST.get('username')
                        password = request.POST.get('password')
                        email = request.POST.get('email')
                        phonenumber = request.POST.get('phoneNumber')
                except ValueError:
                        pass


                # testing input field validity
                input_field_test = Input_field_test()  # save memory, only instantiate class object once
                username_validity = input_field_test.username(username)
                password_validity = input_field_test.password(password)
                email_validity = input_field_test.email(email)
                phonenumber_validity = input_field_test.phonenumber(phonenumber)

                if len(username_validity)==1 and len(password_validity)==1 and len(email_validity)==1 and len(phonenumber_validity)==1:
                        # input fields are valid
                        user=User.objects.filter(username=username)
                        if user.exists()==False:
                                user = User.objects.create_user(username=username, email=email, password=password, phoneNumber=phonenumber)
                                user.is_active = True
                                user.save()
                                return HttpResponseRedirect(reverse("login:index"))

                        else:
                                # User already exists
                                error_message = error_message_user_exist
                else:
                        # input fields are not valid
                        empty_input_state = False
                        invalid_input_state = False

                        for i in username_validity:
                                if i == "empty":
                                        empty_input_state = True
                                elif i == "invalid value":
                                        invalid_input_state = True
                        for i in password_validity:
                                if i == "empty":
                                        empty_input_state = True
                                elif i == "invalid value":
                                        invalid_input_state = True
                        for i in email_validity:
                                if i == "empty":
                                        empty_input_state = True
                                elif i == "invalid value":
                                        invalid_input_state = True
                        for i in phonenumber_validity:
                                if i == "empty":
                                        empty_input_state = True
                                elif i == "invalid value":
                                        invalid_input_state = True

                        if empty_input_state:
                                # input fields are empty
                                error_message = error_message_empty_input
                        elif invalid_input_state:
                                # input fields have invalid input
                                error_message = error_message_invalid_input

                messages.error(request, error_message)

	# if a GET (or any other method) we'll create a blank form
	else:
		form = UserForm()

	return render(request, 'createuser/user.html', {'error_message':None})
