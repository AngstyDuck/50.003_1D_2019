from audioop import reverse

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from createuser.models import Extended_User as User

def home(request):
        error_message = None
        if (request.user.is_authenticated):
                # user is logged in
                if (request.user.is_superuser):
                        # user is superuser
			username = request.user.get_username()
			ticketlist = len(All_Tickets.objects.all())
			unresolevdlist = len(All_Tickets.objects.all().filter(resolved_by=None))
			unreadlist = len(All_Tickets.objects.all().filter(read_by=None))
			try:
				task = round((unresolevdlist / ticketlist)*100,2)
			except ZeroDivisionError:
				return render(request, 'noticketadmin.html' )

			outputList = sort_ticket_list(request, All_Tickets.objects.all(), request.user.is_superuser)
			return render(request, 'dashboardadmin.html', {"list": outputList,'error_message':error_message, 'ticket':ticketlist, "unresolved":unresolvedlist, "unread":unreadlist, 'unread':unreadlist,'task':task,"username":username})

                else:
                        # user is normal user
			username = request.user.id
			print(request.user.email)
			outputList = sort_ticket_list(request, All_Tickets.objects.all().filter(creator=request.user.id),
				request.user.is_superuser)
			print(len(outputList))
			return render(request, 'dashboarduser.html', {'error_message':error_message,'username':request.user.get_username(), "list":outputList})

        else:
                # user has not logged in, redirect to login page
                return HttpResponseRedirect(reverse('login:index'))

