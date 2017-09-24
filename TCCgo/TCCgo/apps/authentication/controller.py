from django.db import models
from pprint import pprint
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
        print("User " + username + " criada.")
        return new_user;

    def request_create(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        enroll_number = request.POST['enroll_number']
        return self.create(username, email, password, enroll_number)
