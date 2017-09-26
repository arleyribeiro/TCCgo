from django.db import models

class Fragment(models.Model):
	content = models.CharField(max_length=50, null=False, blank=False)
	position = models.IntegerField()
	line = models.IntegerField()
	# inconsistency_id_fk = models.ForeignKey(
    #     'Inconsistency',
    #     on_delete = models.CASCADE,
    #     blank=False,
    #     null=False,
    # )

class Text(models.Model):
	content = models.IntegerField()
	title = models.CharField(max_length=50, null=False, blank=False)
    # TODO: Ver isso no lab
	# fragment_id_fk = models.ForeignKey(
    #     'Fragment',
    #     on_delete = models.CASCADE,
    #     blank=False,
    #     null=False,
    # )

    # fragment_inconsistency_id_fk = models.ForeignKey(
    #     'Inconsistency',
    #     on_delete = models.SET_NULL,
    #     blank=False,
    #     null=False,
    # )
