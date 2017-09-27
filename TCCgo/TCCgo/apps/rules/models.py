from django.db import models

from TCCgo.apps.authentication.models import User

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

class Inconsistency(models.Model):
    rule_id_fk = models.ForeignKey(
        'Rule',
        on_delete = models.CASCADE,
        blank=False,
        null=False,
    )
    # TODO: Ver isso na sala
    # fragment_id_fk = models.ForeignKey(
    #     'Fragment',
    #     on_delete = models.SET_NULL,
    #     blank=False,
    #     null=False,
    # )
    # user_id_fk = models.ForeignKey(
    #     'User',
    #     on_delete = models.CASCADE,
    #     blank=False,
    #     null=False,
    # )
    inconsistencyType_id_fk = models.ForeignKey(
        'InconsistencyType',
        on_delete = models.CASCADE,
        blank=False,
        null=False,
    )

class InconsistencyType(models.Model):
    type = models.CharField(max_length=50)
