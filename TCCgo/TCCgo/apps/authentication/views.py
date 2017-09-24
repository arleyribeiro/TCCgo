from django.shortcuts import render

from .controller import (
    UserController
)

def index(request):
    return render(request, 'index.html');

def register(request):
    return render(request, 'register.html');

def create_user(request):
    user_controller = UserController()
    user_controller.request_create(request)
    return render(request, 'index.html');
