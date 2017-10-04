from django.db import models

from TCCgo.apps.authentication.models import User
from TCCgo.apps.text.models import Fragment

class RuleType(models.Model):
    """It's an enum for the Rule field."""
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class Rule(models.Model):
    """Has a pattern and a warning. Is searched in the text while scanning it."""
    pattern = models.CharField(max_length=50, blank=False, null=False)
    warning = models.TextField(max_length=100, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False, db_index=True, unique=True)
    # weight = models.IntegerField() # Decide if this field is gonna be keep
    date = models.DateField(auto_now=True)
    rule_type = models.ForeignKey(RuleType, on_delete = models.PROTECT, blank=False, null=False)
    user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=False, null=True)

    def __str__(self):
        return self.name

class InconsistencyType(models.Model):
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class Inconsistency(models.Model):
    fragment = models.ForeignKey(Fragment, on_delete = models.PROTECT, blank=False, null=False)
    rule = models.ForeignKey(Rule, on_delete = models.PROTECT, blank=False, null=False)
    inconsistency_type = models.ForeignKey(InconsistencyType, on_delete = models.PROTECT, blank=False, null=False)
    user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=False, null=True)

    class Meta():
        verbose_name = "Inconsistency"
        verbose_name_plural = "Inconsistencies" # Without this it's called Inconsistencys, IT'S WRONG
