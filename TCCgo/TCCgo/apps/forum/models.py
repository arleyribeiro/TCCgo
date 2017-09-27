from django.db import models
from TCCgo.apps.authentication.models import User

class Topic(models.Model):
	title = models.CharField(max_length=150, blank=False, null=False)
	message = models.TextField(blank=False, null=False)
	date = models.DateField(auto_now=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE,blank=False, null=False)

class Post(models.Model):
	body = models.TextField()
	index = models.IntegerField()
	date = models.DateField(auto_now=True)
	reply = models.ForeignKey('self', on_delete = models.SET_NULL, blank=True, null=True)
	topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=False, null=False)
