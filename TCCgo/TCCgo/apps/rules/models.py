from django.db import models

# Create your models here.
class RuleManager(models.Manager):

    def create_rule(self, pattern, warning, name, weight, type):
        """ Create a rule and save it to the database."""
        new_rule = Rule(pattern=pattern, warning=warning, name=name, weigth=weight)
        new_rule.rule_type_fk = RuleType.objects.get(type=type)
        new_rule.save()
        print("Regra " + name + " criada.")
        return new_rule;

    def delete_rule(self, name):
        """ Given a rule name, delete it from the database."""
        try:
            rule = self.get(name=name)
            rule.delete()
            print("Regra " + name + "deletada.")
            return True
        except Rule.DoesNotExists:
            print("A regra digitada não existe")
            return None

class Rule(models.Model):
    """Has a pattern and a warning. Is searched in the text while scanning it."""
    pattern = models.CharField(max_length=50, blank=False, null=False)
    warning = models.CharField(max_length=100, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False, db_index=True, unique=True)
    weight = models.IntegerField()
    date = models.DateField(auto_now=True)
    rule_type_fk = models.ForeignKey(
        'RuleType',
        on_delete = models.SET_NULL,
        blank=False,
        null=True,
    )

    objects = RuleManager()

class RuleType(models.Model):
    """It's an enum for the Rule field."""
    type = models.CharField(max_length=50)
