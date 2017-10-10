import json
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from pprint import pprint

from .controller import (
    TextController
)
from .models import (
    Text, Fragment
)


# Create your views here.
def text_page(request):
	return render(request, 'submit.html')

def submit_text(request):
	text_controller = TextController()
	status = text_controller.request_create(request)
	if status == 200:
		return HttpResponse('Sucesso')
	else:
		return HttpResponse('Falha views.py')
