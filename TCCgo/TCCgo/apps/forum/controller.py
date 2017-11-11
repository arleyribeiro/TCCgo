from django.db import models
from django.forms import model_to_dict
from django.db import models
from django.db.models import Q
from django.contrib.auth import login as auth_login

import json


from .models import (
    Topic, Post
)

class TopicController(object):
    def __init__(self):
        pass

    def create(self, title, message, user):
        if (title is not None and message is not None):
            new_topic = Topic(title = title, message = message, user = user)
            new_topic.save()
            dict_text = model_to_dict(new_topic, fields=["id", "title", "message"])
            return dict_text
        else:
            return 300

    def request_filter(self, request):
        """ return filtered texts from request """
        filter_json = json.loads(request.body.decode('utf-8'))
        filter = filter_json['search_topic']
        #topics = TextController.get_all(request.user)
        topics = Topic.objects.filter(Q(title__icontains=filter) | Q(message__icontains=filter))
        return topics

    def request_create(self, request):
        user = request.user
        if user.is_authenticated :
            if user != None:
                    body_json = json.loads(request.body.decode('utf-8'))
                    topic_json = body_json['topic']

                    title = topic_json['title']
                    message = topic_json['message']
                    print(title+'   '+ message)
                    result = self.create(title, message,user)

                    return {'status':200, 'result':result}
        return {'status':300, 'result':[]}


    def get_all(request):
        topics = Topic.objects.all()
        dict_texts = []
        for topic in topics:
            dict_text = model_to_dict(topic, fields = ["id","title", "message"])
            dict_text["message"] = dict_text["message"].splitlines()[0]
            dict_texts.append(dict_text)
        return dict_texts
