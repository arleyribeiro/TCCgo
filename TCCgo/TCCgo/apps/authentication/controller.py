from django.db import models
from django.forms import model_to_dict
from pprint import pprint
import json
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

    def update(self, session_user_id, username, email, enroll_number):
        current_user = User.objects.get(pk=session_user_id)
        if current_user != None:
            current_user.username = username
            current_user.email = email
            current_user.enroll_number = enroll_number
            current_user.save()
        return current_user

    def delete(self, session_user_id):
        current_user = User.objects.get(pk=session_user_id)
        if current_user != None:
            current_user.remove()
            return True
        else:
            return False

    def get_logged_user(self, session_user_id):
        current_user = User.objects.get(pk=session_user_id)
        return current_user

    def request_create(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        enroll_number = request.POST['enroll_number']
        return self.create(username, email, password, enroll_number)

    def request_update(self, request):
        if request.user.is_authenticated :
            session_user = request.user
            if session_user != None:
                session_user_id = session_user.id
                user_json = json.loads(request.body.decode('utf-8'))
                username = user_json['username']
                email = user_json['email']
                enroll_number = user_json['enroll_number']
                updated_user =  self.update(session_user_id, username, email, enroll_number)
                dict_updated_user = model_to_dict(updated_user, fields = ["username", "email", "enroll_number"])
                return dict_updated_user
            else:
                return False
        else: return False

    def request_delete(self, request):
        session_user = request.user
        if session_user != None:
            session_user_id = session_user.id
            return self.delete(session_user_id)
        else:
            return None

    def request_get_logged_user(self, request):
        if request.user.is_authenticated :
            session_user = request.user
            if session_user != None:
                session_user_id = session_user.id
                logged_user = self.get_logged_user(session_user_id)
                dict_logged_user = model_to_dict(logged_user, fields = ["username", "email", "enroll_number"])
                return dict_logged_user
            else:
                return False
        else:
            return False
