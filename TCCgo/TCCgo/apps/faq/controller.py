from .models import Question

class QuestionController(object):
	def get_all():
		questions = Question.objects.all()
		return questions
