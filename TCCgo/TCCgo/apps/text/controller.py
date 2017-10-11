from django.db import models
from django.forms import model_to_dict
from django.db import models
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
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
                print("json de texto: "+ request.body.decode('utf-8'))
                title = request.POST.get("text_title", "titulo")
                content = request.POST.get("text_content", "conteudo")
                user = request.user

                # text_json = json.loads(request.body.decode('utf-8'))
                # title = text_json['title']
                # content = text_json['content']
                #print("titulo" + title + "\ncontent : "+ content)

                new_text = self.create(title, content, user)
                dict_text = model_to_dict(new_text, fields = ["title", "content"])

                return 200
            else:
                return False
        else: return False


    def get_all():
        texts = Text.objects.all()
        return texts

class FragmentController(object):

    def create(self, content, position, text):
        new_fragment = Fragment(content=content, position=position, text=text)
        new_fragment.save()
        return new_fragment
