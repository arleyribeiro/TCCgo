from django.db import models
from django.forms import model_to_dict
from django.db import models
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.db.models import Q
from TCCgo.apps.rules.models import Rule
from TCCgo.apps.rules.models import Inconsistency
from TCCgo.apps.rules.models import InconsistencyType
import json
import re
import pprint

from .models import (
    Text, Fragment
)

class TextController(object):
    def __init__(self):
        pass

    def process_text(self, text, rules, user):
        line = 1
        inconsistency_type = InconsistencyType.objects.all().filter(type="nova")[0]
        sentences = re.split('; |[.?!]', text.content)
        result = []
        for sentence in sentences:
            if '\n' in sentence:
                line = line + 1
            fragment = Fragment(content = sentence, position = line, text = text)
            fragment.save()
            dict_fragment = model_to_dict(fragment, fields = ["id","content", "position"])
            for rule in rules:
                pattern = re.compile(rule.pattern)
                inconsistencies = []
                if pattern.search(sentence):
                    inconsistency = Inconsistency(rule = rule, fragment = fragment, user = user, inconsistency_type=inconsistency_type)
                    inconsistency.save()
                    dict_inconsistency = model_to_dict(inconsistency, fields=["id","inconsistencyType"])
                    dict_inconsistency['rule'] = model_to_dict(rule, fields=["id", "pattern", "warning","name", "rule_type"])
                    # dict_inconsistency['fragment'] = model_to_dict(fragment, fields=["id", "content", "position"])
                    inconsistencies.append(dict_inconsistency)

            result.append({
                'fragment': dict_fragment,
                'inconsistencies': inconsistencies
            })
        return result


    def create(self, title, content, list_rules, user):
        """create a text and save it to database"""
        texts = Text.objects.all().filter(user=user, title=title)
        if texts:
            raise Exception('Já existe esse título no banco')
        new_text = Text(title=title, content=content, user=user)
        new_text.save()

        #modificar para pegar as regras da chamada

        rules = Rule.objects.all().filter(id__in=list_rules)
        result = self.process_text(new_text, rules, user)
        return result

    def get_all(user):
        """ return all texts from databade """
        texts = Text.objects.all().filter(user=user)
        dict_texts = []
        for text in texts:
            dict_text = model_to_dict(text, fields = ["id","title", "content"])
            dict_text["content"] = dict_text["content"].splitlines()[0]
            dict_texts.append(dict_text)
        return dict_texts

    def get(self, user=None, title=None, pk=None): # Se o models estiver certo TMJ !
        """ Given a rule name or id, return it if exists """
        try:
            if(user is not None):
                text = Text.objects.get(user=user, title=title)
            elif(title is not None):
                text = Text.objects.get(title=title)
            elif(pk is not None):
                text = Text.objects.get(pk=pk)
            else:
                print("Nenhum parâmentro foi passado para essa função.")
                text = None
            return text
        except Text.DoesNotExist:
            print("O nome ou id de regra não existe.\n")
            return None

    def get_all_t(user):
          """ return all texts from databade """
          texts = Text.objects.all().filter(user=user)
          return texts

    def delete(self, user, title=None):
        """delete a text from database
        200 -> delete success
        300 -> delete error
        501 -> user error
        """
        text = self.get(user=user, title=title)
        if title is not None:
            if(user == text.user):
                print(title)
                text = TextController.get_all_t(user).filter(title=title)
                if text:
                    text.delete()
                    return 200
            else:
                print("Um usuário não pode deletar o texto de outro")
                return 501
        return 300

    def update(self, pk, title, content):
        text = self.get(pk=pk)
        setattr(text, 'title', title)
        setattr(text, 'content', content)
        text.save()
        return text



    def request_create(self, request):
        """ Create text from request """
        user = request.user
        if user.is_authenticated :
            if user != None:
                try:
                    body_json = json.loads(request.body.decode('utf-8'))
                    text_json = body_json['text']
                    list_json = body_json['private_rules']+body_json['public_rules']

                    title = text_json['title']
                    content = text_json['content']

                    if not title:
                        raise ValueError('str titulo vazio')
                    if not content:
                        raise ValueError('str conteudo vazio')

                    result = self.create(title, content, list_json, user)

                    return {'status':200, 'result':result}

                except ValueError as e:
                    print ("str vazia")
                except:
                    print("erro: titulo repetido")
        return {'status':300, 'result':[]}

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
                    if success == 200:
                        return 200
                    elif success == 300:
                        return 300;
                    else:
                        return 501;
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

    def request_get(self, request):
        get_json = json.loads(request.body.decode('utf-8'))
        text = self.get(pk=get_json['pk'])
        return text

    def update_request(self, request):
        """ update """
        update_json = json.loads(request.body.decode('utf-8'))
        pk = update_json['pk']
        title = update_json['title']
        content = update_json['content']
        text = self.update(pk, title, content)
        return text

class FragmentController(object):

    def create(self, content, position, text):
        new_fragment = Fragment(content=content, position=position, text=text)
        new_fragment.save()
        return new_fragment
