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
    query_set = RuleController.get_all(request.user)
    data = serializers.serialize('json', query_set)
    return JsonResponse(data, safe=False)

def create_rule(request):
    # """Create a rule from a post form in rule_list.html"""
    # rule_name = request.POST.get('rule_name')
    # rule_pattern = request.POST.get('rule_pattern')
    # rule_warning = request.POST.get('rule_warning')
    # print("Padrao da regra: " + rule_name)
    # print("Padrao da regra: " + rule_warning)
    # print("Padrao da regra: " + rule_pattern)
    # RuleController.create(rule_pattern, rule_warning, rule_name, 5, 'Gramatical')
    RuleController.create_with_request(request)
    result = {}
    result['status'] = "Success"
    response = json.dumps(result)
    return JsonResponse(response, safe=False)
