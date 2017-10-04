from django.db import models

from .models import (
    Rule, RuleType
)

class RuleController(object):

    def __init__(self):
        pass

    def create(pattern, warning, name, type, user):
        """ Create a rule and save it to the database."""
        new_rule = Rule(pattern=pattern, warning=warning, name=name, user=user)
        new_rule.rule_type = RuleType.objects.get(type=type)
        new_rule.save()
        print("Regra " + name + " criada.")
        return new_rule;

    def delete(id):
        """ Given a rule name, delete it from the database."""
        try:
            rule = self.get(id=id)
            rule.delete()
            print("Regra " + name + "deletada.\n")
            return True
        except Rule.DoesNotExists:
            print("A regra digitada não existe.\n")
            return True

    def get(id):
        """Given a rule name, return it if exists."""
        try:
            rule = RuleType.objects.get(id=id)
            return rule
        except Rule.DoesNotExists:
            print("O tipo de regra digitado não existe.\n")
            return None

    def get_all(user):
        """Return all Rules in the database"""
        all_rules = Rule.objects.all()
        all_rules = Rule.objects.all().filter(user=user)
        return all_rules

    def create_with_request(request):
        # TODO: doesn't work
        name = request.POST.get('rule_name')
        pattern = request.POST.get('rule_pattern')
        warning = request.POST.get('rule_warning')
        rule_type = 'Gramatical'
        user = request.user
        return RuleController.create(pattern, warning, name, rule_type, user)


class RuleTypeController(object):
    def create(type):
        """ Create a ruleType and save it to the database"""
        new_rule_type = RuleType(type=type)
        new_rule_type.save()
        return new_rule_type

    def delete(id):
        try:
            rule_type = RuleType.objects.get(id=id)
            rule_type.delete()
            print("Tipo de regra " + type + " deletado.\n")
            return True
        except RuleType.DoesNotExists:
            print("O tipo de regra digitado não existe.\n")
            return False

    def get(id):
        try:
            rule_type = RuleType.objects.get(id=id)
            return rule_type
        except RuleType.DoesNotExists:
            print("O tipo de regra digitado não existe.\n")
            return None

    def get_all():
        """Retunr all rule types in the database"""
        all_types = RuleType.objects.all()
        for rule_type in all_types:
            print(rule_type.type + "\n")
        return all_types
