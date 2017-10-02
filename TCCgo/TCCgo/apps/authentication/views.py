from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect
from django.http import HttpResponse

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
    user_controller.request_delete(request)
    return render(request, 'index.html');

def login(request):
    status = UserController().request_login(request)
    if(status == 200):
        return HttpResponseRedirect("/")
    elif(status == 300):
        return HttpResponse('Invalid Login'+' '+email+' '+password +' <p> não funciona para rute, a documentação é inimiga da perfeicao')
    else:
        return render(request,'login.html')


def logout(request):
	auth_logout(request)
	print('log')
	return HttpResponseRedirect("/")
