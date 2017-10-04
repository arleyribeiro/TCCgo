from django.contrib import admin

from .models import *

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer']

admin.site.register(Question, QuestionAdmin)
