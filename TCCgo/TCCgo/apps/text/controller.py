from django.db import models
from django.forms import model_to_dict
from django.db import models
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.db.models import Q
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
        """ Create text from request """
        user = request.user
        if user.is_authenticated :
            if user != None:
                try:
                    text_json = json.loads(request.body.decode('utf-8'))
                    title = text_json['title']
                    content = text_json['content']

                    if not title: raise ValueError('str titulo vazio')
                    if not content: raise ValueError('str conteudo vazio')

                    new_text = self.create(title, content, user)
                    dict_text = model_to_dict(new_text, fields = ["title", "content"])
                    return 200

                except ValueError as e:
                    print ("str vazia")
        return 300

    def request_filter(self, request):
        """ return filtered texts from request """
        filter_json = json.loads(request.body.decode('utf-8'))
        filter = filter_json['search_text']
        texts = Text.objects.filter(Q(title__icontains=filter) | Q(content__icontains=filter))
        return texts

    def get_all():
        """ return all texts from databade """
        texts = Text.objects.all()
        return texts

class FragmentController(object):

    def create(self, content, position, text):
        new_fragment = Fragment(content=content, position=position, text=text)
        new_fragment.save()
        return new_fragment
