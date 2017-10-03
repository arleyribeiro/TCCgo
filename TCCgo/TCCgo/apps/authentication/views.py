import json
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from pprint import pprint

from .controller import (
    UserController
)
from .models import (
    User
)

def index(request):
    return render(request, 'index.html');

def register(request):
    return render(request, 'register.html');

def get_logged_user(request):
    user_controller = UserController()
    logged_user = user_controller.request_get_logged_user(request)
    return JsonResponse(logged_user, safe=False)

def create_user(request):
    user_controller = UserController()
    user_controller.request_create(request)
    return render(request, 'index.html');

def delete_user(request):
    user_controller = UserController()
    user_controller.request_delete(request)
    return render(request, 'index.html');

def update_user(request):
    user_controller = UserController()
    updated_user = user_controller.request_update(request)
    return JsonResponse(updated_user, safe=False)

def login(request):
	if request.method == 'POST':
		email = password = ''
		email = request.POST.get('email','')
		password = request.POST.get('password','')
		user = User.authenticate(request, email=email, password=password)

		print (user)
		if user is not None:
			if user.is_active:
				auth_login(request,user)
				return HttpResponseRedirect("/")
		else:
			return HttpResponse('Invalid Login'+' '+email+' '+password +' <p> não funciona para rute, a documentação é inimiga da perfeicao')
	else:
		return render(request,'login.html')

def logout(request):
	auth_logout(request)
	print('log')
	return HttpResponseRedirect("/")
