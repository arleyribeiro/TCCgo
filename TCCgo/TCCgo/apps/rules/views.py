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

def create_rule(request):
    """Create a rule from a post form in rule_list.html"""
    data = {}
    print(request.POST['rule_name'])
    # The line below doesn't work
    # TODO: FIX IT
    # data['rule'] = RuleController.create_with_request(RuleController(), request)
    data['status'] = "Success"
    response = json.dumps(data)
    return JsonResponse(response, safe=False)
