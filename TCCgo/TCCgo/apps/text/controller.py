from django.db import models
from django.forms import model_to_dict
from django.db import models
from django.contrib.auth import login as auth_login
import json

from .models import (
    Text, Fragment
)

class TextController(object):
    def __init__(self):
        pass


    def create(self, title, content, user):
        """create a text and save it to database"""
        new_text = Text(title=title, content=content, user=user)
        new_text.save()
        return new_text

    def request_create(self, request):
        if request.user.is_authenticated :
            session_user = request.user
            if session_user != None:
                session_user_id = session_user.id
                print("Merda de json de texto: "+ request.body.decode('utf-8'))
                text_json = json.loads(request.body.decode('utf-8'))
                #title = text_json['title']
                #content = text_json['content']
                #new_text = self.create(self, title, content, user)
                #dict_text = model_to_dict(updated_user, fields = ["title", "content"])
                #return dict_text
            else:
                return False
        else: return False

        #title = request.POST.get('text_title')
        #content = request.POST.get('text_content')
        #new

    def get_all():
        text = Text.objects.all()
        return text

class FragmentController(object):

    def create(self, content, position, text):
        new_fragment = Fragment(content=content, position=position, text=text)
        new_fragment.save()
        return new_fragment
