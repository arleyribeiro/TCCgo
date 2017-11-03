import json
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from pprint import pprint

from .controller import (
    TextController
)
from .models import (
    Text, Fragment
)

def index(request):
    return render(request, 'index.html');

# Create your views here.
def text_page(request):
	return render(request, 'submit.html')

def all_texts_page(request):
	return render(request, 'list.html')

def edit_text_page(request):
    """ Render the edit text page """
    #print("Valor do pk " + pk)
    return render(request, 'edit.html')

def create_text(request):
    """ create a new text """
    status = TextController().request_create(request)
    if status == 200:
        return JsonResponse({'success':True, 'url':'127.0.0.1:8000'}, safe=False)
    else:
        return JsonResponse({'success':False}, safe=False)

def delete_text(request):
    """ Delete text from request
    200 -> delete success
    300 -> delete error
    501 -> user error
    """
    status = TextController().request_delete(request)
    if status == 200:
        return JsonResponse({'error':200}, safe=False)
    elif status == 501:
        return JsonResponse({'error':501}, safe=False)
    else:
        return JsonResponse({'error':300}, safe=False)

def update_text(request):
    """ Update a text """
    controller = TextController()
    text = controller.update_request(request)
    return JsonResponse({'text' : model_to_dict(text)}, safe=False)

def get_text(request):
    """Return a text given it pk """
    controller = TextController()
    text = controller.request_get(request)
    print(text)
    return JsonResponse({'text' : model_to_dict(text)}, safe=False)

def get_all_texts(request):
    """ Return all texts"""
    data = TextController.get_all(request.user)
    #print(query_set[0].content)
    #data = serializers.serialize('json', query_set)
    return JsonResponse(data, safe=False)

def filter_texts(request):
    """ Return a filtered by name set of texts"""
    query_set = TextController().request_filter(request)
    response =  serializers.serialize('json', query_set)
    print(response)
    return JsonResponse(response, safe=False)
