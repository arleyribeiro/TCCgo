from .models import Question

class QuestionController(object):
    def create(question, answer):
        """ Create a question and save it to the database."""
        new_question = Question(question=question, answer = answer)
        new_question.save()
        print("Questão salva no banco de dados")
        return new_question

    def get_all():
        questions = Question.objects.all()
        return questions
