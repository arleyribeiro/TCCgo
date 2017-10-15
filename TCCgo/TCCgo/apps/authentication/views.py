import json
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate
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

def password(request):
    return render(request, 'password.html');

def get_logged_user(request):
    user_controller = UserController()
    logged_user = user_controller.request_get_logged_user(request)
    return JsonResponse(logged_user, safe=False)

def check_unique_email(request):
    user_controller = UserController()
    is_unique = user_controller.request_check_unique_email(request)
    return JsonResponse(is_unique, safe=False)

def create_user(request):
    user_controller = UserController()
    status = user_controller.request_create(request)
    if  status == 200:
        return HttpResponseRedirect("/")
    elif status == 300:
        return HttpResponse('Falha ao registrar novo usuário!')

def delete_user(request):
    user_controller = UserController()
    status = user_controller.request_delete(request)
    if status == 200:
        auth_logout(request)
        return JsonResponse({'success':True, 'url':'127.0.0.1:8000'}, safe=False)
    elif status == 300:
        return JsonResponse({'success':False}, safe=False)

def update_user(request):
    user_controller = UserController()
    updated_user = user_controller.request_update(request)
    return JsonResponse(updated_user, safe=False)

def change_password(request):
    user_controller = UserController()
    response = user_controller.request_change_password(request)
    return JsonResponse(response, safe=False)


def login(request):
    return render(request, 'login.html')

def check_login(request):

    user_controller = UserController();
    status = user_controller.request_check_login(request)

    if(status == 200):
        return JsonResponse({'success':True, 'url':'http://localhost:8000'}, safe=False)
    else:
        return JsonResponse({'success':False,'url':[]}, safe=False)

def logout(request):
	auth_logout(request)
	print('log')
	return HttpResponseRedirect("/")
