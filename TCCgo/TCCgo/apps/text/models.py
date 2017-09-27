from django.db import models
from TCCgo.apps.authentication.models import User

class Text(models.Model):
	content = models.TextField(null=False, blank=False)
	title = models.CharField(max_length=150, null=True, blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

class Fragment(models.Model):
	content = models.TextField(null=False, blank=False)
	position = models.IntegerField(null=False, blank=False)
	text = models.ForeignKey(Text, on_delete=models.CASCADE, null=False, blank=False)
