from django.db import models
from django.forms import model_to_dict
from django.db import models
from django.db.models import Q
from django.contrib.auth import login as auth_login

import json

from TCCgo.apps.authentication.models import User

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

    def get(self, pk=None):
        try:
            if(pk is not None):
                topic = Topic.objects.get(pk=pk)
            else:
                print("Nenhum parâmentro foi passado para essa função.")
                topic = None
            return topic
        except Topic.DoesNotExist:
                print("O nome ou id de regra não existe.\n")
                return None


    def request_get(self, request):
        get_json = json.loads(request.body.decode('utf-8'))
        topic = self.get(pk=get_json['pk'])
        return topic


class PostController(object):
    def __init__(self):
        pass

    def create(self, body, reply, topic, user):
        if (body is not None and topic is not None):
            new_post = Post(body=body, reply=reply, topic=topic, user=user)
            new_post.save()
            return 200
        else:
            return 300

    def get(self, pk=None):
        try:
            if(pk is not None):
                post = Post.objects.get(pk=pk)
            else:
                print("Nenhum parâmentro foi passado para essa função.")
                post = None
            return post
        except Post.DoesNotExist:
                print("O nome ou id de regra não existe.\n")
                return None


    def request_create(self, request):
        controller = TopicController()

        user = request.user
        if user.is_authenticated :
            if user != None:
                    post_json = json.loads(request.body.decode('utf-8'))
                    #post_json = body_json['post']

                    body = post_json['body']
                    # reply = post_json['reply']
                    # reply = self.get(reply)
                    reply = None

                    topic = post_json['topic']
                    topic = controller.get(topic)
                    user1 = post_json['user']
                    #print("\n \n\n\n " + user1)
                    user = User.objects.get(pk=user1)
                    result = self.create(body,reply, topic, user)

                    return result
        return 300

    def request_get_posts(self, request):
        post_json = json.loads(request.body.decode('utf-8'))
        topic = post_json['topic']

        posts = Post.objects.filter(topic=topic).order_by('date')

        dict_texts = []
        for post in posts:
            print(post.user)
            dict_text = model_to_dict(post, fields = ["id","body", "reply","date","topic", "user"])
            dict_text['user'] = model_to_dict(post.user, fields = ["id","username"])
            dict_texts.append(dict_text)
            print(dict_texts[0]['user'])
        return dict_texts
