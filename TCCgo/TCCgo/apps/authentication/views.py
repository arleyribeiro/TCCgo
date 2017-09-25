from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseRedirect

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

