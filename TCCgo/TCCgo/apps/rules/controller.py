from django.db import models

from .models import (
    Rule, RuleType
)

class RuleController(object):

    def __init__(self):
        pass

    def create(self, pattern, warning, name, scope, type, user):
        """ Create a rule and save it to the database """
        rule = self.get(name=name)
        if(rule is None): # Rule name doesn't exists in the database
            new_rule = Rule(pattern=pattern, warning=warning, name=name, scope=scope, user=user)
            new_rule.rule_type = RuleType.objects.get(type=type)
            new_rule.save()
            print("Regra " + name + " criada.")
            return new_rule;
        else: # Name already exists
            print("Esse nome de regra já existe no sistema.")
            return None


    def delete( self, user, id=None, name=None):
        """ Given a rule name or id, delete it from the database """
        rule = self.get(id=id, name=name)
        if(rule is not None):
            if(user == rule.user):
                rule.delete()
                print("Regra " + name + "deletada.\n")
                return True
            else:
                print("Um usuário não pode deletar a regra de outro")
                return False
        else:
            print("A regra digitada não existe.\n")
            return True

    def get(self, id=None, name=None):
        """ Given a rule name or id, return it if exists """
        try:
            if(id is not None):
                rule = Rule.objects.get(id=id)
            elif(name is not None):
                rule = Rule.objects.get(name=name)
            else:
                print("Nenhum parâmentro foi passado para essa função.")
                rule = None
            return rule
        except Rule.DoesNotExist:
            print("O nome ou id de regra não existe.\n")
            return None

    def get_all(self, user):
        """ Return all Rules in the database linked to an especific user """
        all_rules = Rule.objects.all()
        all_rules = Rule.objects.all().filter(user=user)
        return all_rules

    def create_with_request(self, request):
        """ Given a request, create a rule with the data in it """
        name = request.POST.get('rule_name')
        pattern = request.POST.get('rule_pattern')
        warning = request.POST.get('rule_warning')
        rule_type = request.POST.get('rule_type')
        scope = request.POST.get('rule_scope')
        user = request.user
        return self.create(pattern, warning, name, scope, rule_type, user)


class RuleTypeController(object):
    def create(self, type):
        """ Create a ruleType and save it to the database """
        new_rule_type = RuleType(type=type)
        new_rule_type.save()
        return new_rule_type

    def delete(self, id):
        """ Delete a rule type with the given id """
        rule_type = self.get(id=id)
        if(rule_type is not None):
            rule_type.delete()
            print("Tipo de regra " + type + " deletado.\n")
            return True
        else:
            print("O tipo de regra digitado não existe.\n")
            return False

    def get(self, id):
        """ Return a rule type with the given id """
        try:
            rule_type = RuleType.objects.get(id=id)
            return rule_type
        except RuleType.DoesNotExists:
            print("O tipo de regra digitado não existe.\n")
            return None

    def get_all(self):
        """ Return all rule types in the database """
        all_types = RuleType.objects.all()
        return all_types
