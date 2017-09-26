from django.db import models

class Topic(models.Model):
	title = models.TextField()
	message = models.TextField()
	date = models.DateField(auto_now=True)
	post_id_fk = models.ForeignKey('Post', on_delete = models.CASCADE, blank=False, null=False)

class Post(models.Model):
	body = models.TextField()
	index = models.IntegerField()
	date = models.DateField(auto_now=True)
	post_id_fk = models.ForeignKey('Post', on_delete = models.CASCADE, blank=False, null=True)
