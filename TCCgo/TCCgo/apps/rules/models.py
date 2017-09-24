from django.db import models

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

class RuleType(models.Model):
    """It's an enum for the Rule field."""
    type = models.CharField(max_length=50)
