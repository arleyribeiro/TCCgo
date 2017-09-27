from django.db import models

from TCCgo.apps.authentication.models import User
from TCCgo.apps.text.models import Fragment

class RuleType(models.Model):
    """It's an enum for the Rule field."""
    type = models.CharField(max_length=50)

class Rule(models.Model):
    """Has a pattern and a warning. Is searched in the text while scanning it."""
    pattern = models.CharField(max_length=50, blank=False, null=False)
    warning = models.CharField(max_length=100, blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False, db_index=True, unique=True)
    weight = models.IntegerField()
    date = models.DateField(auto_now=True)
    rule_type = models.ForeignKey(RuleType, on_delete = models.PROTECT, blank=False, null=False)
    user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=False, null=True)

class InconsistencyType(models.Model):
    type = models.CharField(max_length=50)

class Inconsistency(models.Model):
    fragment = models.ForeignKey(Fragment, on_delete = models.PROTECT, blank=False, null=False)
    rule = models.ForeignKey(Rule, on_delete = models.PROTECT, blank=False, null=False)
    inconsistency_type = models.ForeignKey(InconsistencyType, on_delete = models.PROTECT, blank=False, null=False)
    user = models.ForeignKey(User, on_delete = models.SET_NULL, blank=False, null=True)
