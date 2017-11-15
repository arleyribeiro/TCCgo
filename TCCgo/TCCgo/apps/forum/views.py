import json
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.forms import model_to_dict

from .controller import (
	TopicController, PostController
)

from TCCgo.apps.authentication.controller import UserController

# Create your views here.

def forum_page(request):
	return render(request, 'forum.html')

def new_topic(request):
	return render(request, 'new_topic.html')

def view_topic(request):
	return render(request, 'view_topic.html')

def filter_topics(request):
	""" Return a filtered by name set of topics"""
	#print(request.body.decode('utf-8'))
	controller = TopicController()
	query_set = controller.request_filter(request)
	response = {}
	response['filtered_topics'] = list(query_set.values())
	return JsonResponse(response, safe=False)

def create_topic(request):
	topic_controller = TopicController()
	result = topic_controller.request_create(request)
	if result['status'] == 200:
		return JsonResponse({'success':True, 'result':result['result']}, safe=False)
	else:
		return JsonResponse({'success':False, 'result':[]}, safe=False)

def get_all_topics(request):
	""" Return all topics"""
	data = TopicController.get_all(request)
	return JsonResponse(data, safe=False)

def get_topic(request):
    """Return a topic given it pk """
    controller = TopicController()
    topic = controller.request_get(request)
    return JsonResponse({'topic' : model_to_dict(topic)}, safe=False)

def get_user(request):
	controller = UserController()
	user = controller.request_get_user(request)
	return JsonResponse({'user': model_to_dict(user)}, safe=False)


# -------------------- POST ------------------------------------------------------

def create_post(request):
	controller = PostController()
	post = controller.request_create(request)
	if post == 200:
		return JsonResponse({'success' : True}, safe=False)
	else:
		return JsonResponse({'success' : False}, safe=False)

def get_posts(request):
	controller = PostController()
	posts = controller.request_get_posts(request)
	return JsonResponse(posts, safe=False)
