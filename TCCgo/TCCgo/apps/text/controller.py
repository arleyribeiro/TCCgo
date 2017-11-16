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

    def get_processed_text(self, text_id):
        result = []
        text = Text.objects.filter(id=text_id)[0]
        fragments = Fragment.objects.filter(text=text)
        print(len(fragments))
        for fragment in fragments:
            dict_fragment = model_to_dict(fragment, fields = ["id","content", "position"])
            inconsistencies = Inconsistency.objects.filter(fragment=fragment)
            l_inconsistencies = []
            for inconsistency in inconsistencies:
                dict_inconsistency = model_to_dict(inconsistency, fields=["id","inconsistency_type"])
                dict_inconsistency['rule'] = model_to_dict(inconsistency.rule, fields=["id", "pattern", "warning","name", "rule_type"])
                l_inconsistencies.append(dict_inconsistency)
            result.append({
                'fragment': dict_fragment,
                'inconsistencies': l_inconsistencies
            })

        return result

    def process_text(self, text, rules, user):
        line = 1
        inconsistency_type = InconsistencyType.objects.all().filter(type="nova")[0]
        sentences = re.split('; |[.?!]', text.content)
        if(sentences[-1]==''):
            sentences.pop()
        for sentence in sentences:
            if '\n' in sentence:
                line = line + 1
            fragment = Fragment(content = sentence, position = line, text = text)
            fragment.save()
            for rule in rules:
                pattern = re.compile(rule.pattern)
                inconsistencies = []
                if pattern.search(sentence):
                    inconsistency = Inconsistency(rule = rule, fragment = fragment, user = user, inconsistency_type=inconsistency_type)
                    inconsistency.save()

    def rebuild_text(self, sentences):
        new_text = ""
        limit = len(sentences)
        for key in range(limit):
            if key > 0 and sentences[key]['fragment']['position'] > sentences[key-1]['fragment']['position']:
                new_text = new_text + "\n" + sentences[key]['fragment']['content'] + "."
            else:
                new_text = new_text + sentences[key]['fragment']['content'] + "."
        return new_text


    def get_fragment_inconsistencies_by_id(self, sentences, fragment_id):
        fragment = None
        inconsistencies = []
        for sentence in sentences:
            if sentence['fragment']['id'] == fragment_id:
                fragment = sentence['fragment']
                inconsistencies = sentence['inconsistencies']
                break
        return fragment, inconsistencies

    def get_inconsistency_by_id(self, inconsistencies, inconsistency_id):
        incon = None
        for inconsistency in inconsistencies:
            if inconsistency['id'] == inconsistency_id:
                incon = inconsistency
                break
        return incon

    def fix_text(self, text_id, sentences):
        text = Text.objects.filter(id=text_id)[0]
        fragments = Fragment.objects.filter(text=text)
        new_text = self.rebuild_text(sentences)
        text.content = new_text
        text.save()
        for fragment in fragments:
            dict_fragment, dict_inconsistencies = self.get_fragment_inconsistencies_by_id(sentences, fragment.id)
            fragment.content = dict_fragment['content']
            inconsistencies = Inconsistency.objects.filter(fragment=fragment)
            for inconsistency in inconsistencies:
                dict_inconsistency = self.get_inconsistency_by_id(dict_inconsistencies, inconsistency.id)
                inconsistency_type = InconsistencyType.objects.all().filter(id=dict_inconsistency['inconsistency_type'])[0]
                inconsistency.inconsistency_type = inconsistency_type
                inconsistency.save()
            fragment.save()


    def request_fix_text(self, request):
        get_json = json.loads(request.body.decode('utf-8'))
        try:
            self.fix_text(text_id=get_json['id'], sentences=get_json['sentences'])
            return 200
        except Exception as e:
            return 300


    def create(self, title, content, list_rules, user):
        """create a text and save it to database"""
        texts = Text.objects.all().filter(user=user, title=title)
        if texts:
            raise Exception('Já existe esse título no banco')
        new_text = Text(title=title, content=content, user=user)
        new_text.save()
        dict_text = model_to_dict(new_text, fields=["id", "title", "content"])
        #modificar para pegar as regras da chamada

        rules = Rule.objects.all().filter(id__in=list_rules)
        self.process_text(new_text, rules, user)
        return dict_text

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

    def request_get_processed_text(self, request):
        get_json = json.loads(request.body.decode('utf-8'))
        result = self.get_processed_text(text_id=get_json['id'])
        return result

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
