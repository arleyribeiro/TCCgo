import json
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core import serializers
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

def submit_text(request):
	text_controller = TextController()
	status = text_controller.request_create(request)
	if status == 200:
		return JsonResponse({'success':True, 'url':'127.0.0.1:8000'}, safe=False)
	else:
		return JsonResponse({'success':False}, safe=False)

def get_all_texts(request):
	query_set = TextController.get_all()
	data = serializers.serialize('json', query_set)
	#print data
	return JsonResponse(data, safe=False)
