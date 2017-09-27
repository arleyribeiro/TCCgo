from django.shortcuts import render
from .controller import QuestionController
from django.core import serializers

# Create your views here.
def get_all_questions(request):
	data = QuestionController.get_all()
	data = serializers.serialize('json', data)
	return JsonResponse(data, safe=False)

def faq_page(request):
	return render(request, 'faq.html')


