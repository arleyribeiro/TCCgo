import json

from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.forms.models import model_to_dict


from .controller import (
    RuleController, RuleTypeController
)

def rules_list(request):
    """ Render the rules list page """
    return render(request, 'rules_list.html')

def get_all_rules(request):
    """ Return a Json containing all the rules in the database linked to the current user """
    controller = RuleController()
    query_set = controller.get_all(request.user)
    response = {}
    response['rules'] = list(query_set.values())
    return JsonResponse(response, safe=False)

def get_all_types(request):
    """ Return a Json containing all the rule types in the database """
    controller = RuleTypeController()
    query_set = controller.get_all()
    response = {}
    response['types'] = list(query_set.values())
    return JsonResponse(response, safe=False)

def filter_rules(request):
    """ Return a filtered by name set of rules"""
    controller = RuleController()
    query_set = controller.filter_with_request(request)
    response = {}
    response['filtered_rules'] = list(query_set.values())
    return JsonResponse(response, safe=False)

def create_rule(request):
    """ Create a rule, save it to the database and return it to javascript """
    controller = RuleController()
    rule = controller.create_with_request(request)
    response = {}
    if(rule is not None):
        response['status'] = "Success"
        response['new_rule'] = model_to_dict(rule)
    else:
        response['status'] = "False"
    return JsonResponse(response, safe=False)

def delete_rule(request):
    """ Delete a rule passed in the request"""
    controller = RuleController()
    status = controller.delete_with_request(request)
    response = {}
    response['status'] = status
    return JsonResponse(response, safe=False)

def verify_name(request):
    """ Return True if a rule name already exists in database """
    controller = RuleController()
    rule_name = request.GET.get('name')
    rule = controller.get(name=rule_name)
    response = {}
    if(rule is None):
        response['status'] = False
    else:
        response['status'] = True
    return JsonResponse(response, safe=False)
