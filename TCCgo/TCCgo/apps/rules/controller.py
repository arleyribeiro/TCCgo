from django.db import models

from .models import (
    Rule, RuleType
)

class RuleController(object):

    def create(pattern, warning, name, weight, type):
        """ Create a rule and save it to the database."""
        new_rule = Rule(pattern=pattern, warning=warning, name=name, weight=weight)
        new_rule.rule_type_fk = RuleType.objects.get(type=type)
        new_rule.save()
        print("Regra " + name + " criada.")
        return new_rule;

    def delete(name):
        """ Given a rule name, delete it from the database."""
        try:
            rule = self.get(name=name)
            rule.delete()
            print("Regra " + name + "deletada.\n")
            return True
        except Rule.DoesNotExists:
            print("A regra digitada não existe.\n")
            return True

    def get(name):
        """Given a rule name, return it if exists."""
        try:
            rule = RuleType.objects.get(name=name)
            return rule
        except Rule.DoesNotExists:
            print("O tipo de regra digitado não existe.\n")
            return None

    def get_all():
        """Return all Rules in the database"""
        all_rules = Rule.objects.all()
        for rule in all_rules:
            print(rule.name + "\n")
        return all_rules

class RuleTypeController(object):
    def create(type):
        """ Create a ruleType and save it to the database"""
        new_rule_type = RuleType(type=type)
        new_rule_type.save()
        return new_rule_type

    def delete(type):
        try:
            rule_type = RuleType.objects.get(type=type)
            rule_type.delete()
            print("Tipo de regra " + type + " deletado.\n")
            return True
        except RuleType.DoesNotExists:
            print("O tipo de regra digitado não existe.\n")
            return False

    def get(type):
        try:
            rule_type = RuleType.objects.get(type=type)
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
