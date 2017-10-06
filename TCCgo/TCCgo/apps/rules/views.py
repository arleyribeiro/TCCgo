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
    """ Return a Json containing all the rules in the database linked to the current user """
    controller = RuleController()
    query_set = controller.get_all(request.user)
    data = serializers.serialize('json', query_set)
    return JsonResponse(data, safe=False)

def get_all_types(request):
    """ Return a Json containing all the rule types in the database"""
    controller = RuleTypeController()
    query_set = controller.get_all()
    data = serializers.serialize('json', query_set)
    return JsonResponse(data, safe=False)

def create_rule(request):
    controller = RuleController()
    rule = controller.create_with_request(request)
    response = {}
    if(rule is not None):
        response['status'] = "Success"
    else:
        response['status'] = "False"
        # Gambiarra para o angular funcionar
        new_rule['fields'] = rule;
    return JsonResponse(response, safe=False)

def verify_name(request):
    """Return True if a rule name already exists in database"""
    controller = RuleController()
    rule_name = request.GET.get('name')
    print("Nome recebido da regra: " + rule_name)
    rule = controller.get(name=rule_name)
    response = {}
    if(rule is None):
        response['status'] = False
    else:
        response['status'] = True
    return JsonResponse(response, safe=False)
