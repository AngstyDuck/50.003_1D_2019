from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def submit_login(request):
	if request.method == 'GET':
		return HttpResponse("What're you doin here punk")
	elif request.method == 'POST':
		print(request.POST)
		return HttpResponse("POST recevied")
