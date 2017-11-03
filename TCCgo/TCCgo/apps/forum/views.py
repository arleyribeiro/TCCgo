import json
from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers

# Create your views here.

def forum_page(request):
	return render(request, 'forum.html')
