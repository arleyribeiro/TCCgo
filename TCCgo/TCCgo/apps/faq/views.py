import json
from django.shortcuts import render
from django.http import JsonResponse
#from django.http import HttpResponse
from django.core import serializers

from .controller import QuestionController
#from .models import Question

# Create your views here.
def get_all_questions(request):
	query_set = QuestionController.get_all()
	data = serializers.serialize('json', query_set)
	#print data
	return JsonResponse(data, safe=False)

def faq_page(request):
	return render(request, 'faq.html')
