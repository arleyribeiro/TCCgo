import json
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict
from TCCgo.apps.rules.models import Rule
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

def processing_text_page(request):
    """ Render the processing text page """
    return render(request, 'processing.html')

def create_text(request):
    """ create a new text """
    # return JsonResponse({'success':True})
    result = TextController().request_create(request)
    if result['status'] == 200:
        return JsonResponse({'success':True, 'result':result['result']}, safe=False)
    else:
        return JsonResponse({'success':False, 'result':[]}, safe=False)


def delete_text(request):
    """ Delete text from request
    200 -> delete success
    300 -> delete error
    501 -> user error
    """
    # return JsonResponse({'status':200}, safe=False)

    status = TextController().request_delete(request)
    if status == 200:
        return JsonResponse({'status':200}, safe=False)
    elif status == 501:
        return JsonResponse({'status':501}, safe=False)
    else:
        return JsonResponse({'status':300}, safe=False)

def update_text(request):
    """ Update a text """
    controller = TextController()
    text = controller.update_request(request)
    return JsonResponse({'text' : model_to_dict(text)}, safe=False)

def get_text(request):
    """Return a text given it pk """
    controller = TextController()
    text = controller.request_get(request)
    return JsonResponse({'text' : model_to_dict(text)}, safe=False)

def get_processed_text(request):
    controller = TextController()
    result = controller.request_get_processed_text(request)
    return JsonResponse(result, safe=False)

def fix_text(request):
    controller = TextController()
    result = controller.request_fix_text(request)
    return JsonResponse(result, safe=False)

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
