from django.db import models

# Create your models here.
class Question(models.Model):
	#dar migrate cria db
	question = models.CharField(max_length = 255)#maxlength, unique
	answer = models.CharField(max_length = 255)#maxlength, unique

