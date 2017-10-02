from pprint import pprint

from django.db import models
from django.contrib.auth import login as auth_login

from .models import (
    User
)

class UserController(object):
    def __init__(self):
        pass

    def create(self, username, email, password, enroll_number):
        """ Create an user and save it to the database."""
        new_user = User(username = username, email = email, password = password, enroll_number = enroll_number, is_staff = False)
        new_user.save()
        return new_user;

    def update(self, session_user_id, username, email, password, enroll_number):
        current_user = user.objects.get(pk=session_user_id)
        if current_user != None:
            current_user.username = username
            current_user.email = email
            current_user.password = password
            current_user.enroll_number = enroll_number
            current_user.save()
        return current_user

    def delete(self, session_user_id):
        current_user = user.objects.get(pk=session_user_id)
        if current_user != None:
            current_user.remove()
            return True
        else:
            return False


    def request_create(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        enroll_number = request.POST['enroll_number']
        return self.create(username, email, password, enroll_number)

    def request_update(self, request):
        session_user = request.user
        if session_user != None:
            session_user_id = session_user.id
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            enroll_number = request.POST['enroll_number']
            return self.update(session_user_id, username, email, password, enroll_number)
        else:
            return None

    def request_delete(self, request):
        session_user = request.user
        if session_user != None:
            session_user_id = session_user.id
            return self.delete(session_user_id)
        else:
            return None

    def authenticate(self, email=None, password=None):
        print("sdfsdf " +email+ ' ' + password)
        try:
            user = User.objects.get(email=email)
            print("cheguei " + user.password + ' ' + password)
            if password == user.password:
              print('ok')
              return user
            else:
              print('erro')
              return None
        except User.DoesNotExist:
            print('asdfghj')
            return None

    def request_login(self, request):
        if request.method == 'POST':
            email = request.POST.get('email','')
            password = request.POST.get('password','')
            user = UserController.authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request,user)
                    return 200 # Sucess
                else:
                    return 300 # Invalid
            else:
                return 404 # Error
