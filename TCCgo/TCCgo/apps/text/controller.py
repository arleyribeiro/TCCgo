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
        texts = Text.objects.all().filter(user=user, title=title)
        if texts:
            raise Exception('Já existe esse título no banco')
        print("'" + title +"'")
        new_text = Text(title=title, content=content, user=user)
        new_text.save()
        return new_text

    def get_all(user):
        """ return all texts from databade """
        texts = Text.objects.all().filter(user=user)
        return texts

    def get(self, user=None, title=None): # Se o models estiver certo TMJ !
        """ Given a rule name or id, return it if exists """
        try:
            if(user is not None):
                text = Text.objects.get(user=user, title=title)
            elif(title is not None):
                text = Text.objects.get(title=title)
            else:
                print("Nenhum parâmentro foi passado para essa função.")
                text = None
            return text
        except Text.DoesNotExist:
            print("O nome ou id de regra não existe.\n")
            return None

    def delete(self, user, title=None):
        """delete a text from database"""
        text = self.get(user=user, title=title)
        if title is not None:
            if(user == text.user):
                text = TextController.get_all(user).filter(title=title)
                if text:
                    text.delete()
                    return True
            else:
                print("Um usuário não pode deletar o texto de outro")
                return 501
        return False



    def request_create(self, request):
        """ Create text from request """
        user = request.user
        if user.is_authenticated :
            if user != None:
                try:
                    text_json = json.loads(request.body.decode('utf-8'))
                    title = text_json['title']
                    content = text_json['content']

                    if not title:
                        raise ValueError('str titulo vazio')
                    if not content:
                        raise ValueError('str conteudo vazio')

                    new_text = self.create(title, content, user)

                    return 200

                except ValueError as e:
                    print ("str vazia")
                except:
                    print("erro: titulo repetido")
        return 300

    def request_delete(self, request):
        """ delete text from request"""
        user = request.user
        if user.is_authenticated :
            if user is not None:
                try:
                    text_json = json.loads(request.body.decode('utf-8'))
                    title = text_json['text_title']

                    if not title:
                        raise ValueError('str titulo vazio')
                    success = self.delete(user, title)
                    if success:
                        return 200
                except ValueError as e:
                    print ("str vazia")
        return 300

    def request_filter(self, request):
        """ return filtered texts from request """
        filter_json = json.loads(request.body.decode('utf-8'))
        filter = filter_json['search_text']
        texts = TextController.get_all(request.user)
        texts = texts.filter(Q(title__icontains=filter) | Q(content__icontains=filter))
        return texts

class FragmentController(object):

    def create(self, content, position, text):
        new_fragment = Fragment(content=content, position=position, text=text)
        new_fragment.save()
        return new_fragment
