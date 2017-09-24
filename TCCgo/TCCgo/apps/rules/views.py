import json

from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers


from .controller import (
    RuleController, RuleTypeController
)

# Create your views here.
def rules_list(request):
    return render(request, 'rules_list.html')

def get_all_rules(request):
    """ Retunr a Json containing all the rules in the database"""
    query_set = RuleController.get_all()
    data = serializers.serialize('json', query_set)
    return JsonResponse(data, safe=False)
