from django.db import models
from django.forms import model_to_dict
from django.db import models
from django.contrib.auth import login as auth_login
import json

from .models import (
    User
)

class UserController(object):
    def __init__(self):
        pass

    def create(self, username, email, password, check, interest):
        checked = password == check
        try:
            current_user = User.objects.get(email=email)
        except User.DoesNotExist:
            current_user = None
        if current_user == None and checked:
            new_user = User(username = username, email = email, password = password, interest = interest, is_staff = False)
            new_user.save()
            return 200
        else:
            return 300

    def update(self, session_user_id, username, email, interest):
        current_user = User.objects.get(pk=session_user_id)
        if current_user != None:
            current_user.username = username
            current_user.email = email
            current_user.interest = interest
            current_user.save()
        return current_user

    def delete(self, session_user_id):
        current_user = User.objects.get(pk=session_user_id)
        if current_user != None:
            current_user.delete()
            return True
        else:
            return False

    def get_logged_user(self, session_user_id):
        current_user = User.objects.get(pk=session_user_id)
        return current_user

    def check_unique_email(self, email):
        try:
            current_user = User.objects.get(email=email)
        except User.DoesNotExist:
            current_user = None
        return current_user == None

    def change_password(self, request, old_password, new_password, check_password):
        session_user = request.user
        if session_user != None and session_user.is_authenticated:
            if self.authenticate(session_user.email, old_password) != None:
                if new_password == check_password:
                    session_user.password = new_password
                    session_user.save()
                    auth_login(request,session_user)
                    return {'success': True, 'msg': 'Nova senha registrada com sucesso!'};
                else:
                    return {'success': False, 'msg': 'A senha nova e sua confirmação não batem!'};
            else:
                return {'success': False, 'msg': 'A senha antiga está incorreta!'};
        else:
            return {'success': False, 'msg': 'Não é possível alterar senha sem estar logado!'};


    def request_create(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        check = request.POST['check']
        interest = request.POST['interest']
        return self.create(username, email, password, check, interest)

    def request_update(self, request):
        if request.user.is_authenticated :
            session_user = request.user
            if session_user != None:
                session_user_id = session_user.id
                user_json = json.loads(request.body.decode('utf-8'))
                username = user_json['username']
                email = user_json['email']
                interest = user_json['interest']
                updated_user =  self.update(session_user_id, username, email, interest)
                dict_updated_user = model_to_dict(updated_user, fields = ["username", "email", "interest"])
                return dict_updated_user
            else:
                return False
        else: return False

    def request_delete(self, request):
        session_user = request.user
        if session_user != None:
            session_user_id = session_user.id
            if self.delete(session_user_id):
                return 200
            else:
                return 300
        else:
            return 300


    def request_get_logged_user(self, request):
        if request.user.is_authenticated :
            session_user = request.user
            if session_user != None:
                session_user_id = session_user.id
                logged_user = self.get_logged_user(session_user_id)
                dict_logged_user = model_to_dict(logged_user, fields = ["username", "email", "interest"])
                return dict_logged_user
            else:
                return False
        else:
            return False

    def request_check_unique_email(self, request):
        email_json = json.loads(request.body.decode('utf-8'))
        email = email_json['email']
        return self.check_unique_email(email)

    def request_change_password(self, request):
        user_json = json.loads(request.body.decode('utf-8'))
        old_password = user_json['old_password']
        new_password = user_json['new_password']
        check_password = user_json['check_password']
        return self.change_password(request, old_password, new_password, check_password)

    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if password == user.password:
              return user
            else:
              return None
        except User.DoesNotExist:
            return None


    def request_check_login(self, request):
        user_json = json.loads(request.body.decode('utf-8'))
        email = user_json['email']
        password = user_json['password']
        user = UserController.authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request,user)
                return 200 # Sucess
        else:
            return 300 # Invalid
