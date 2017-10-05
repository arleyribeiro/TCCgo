from django.conf.urls import include,url
from . import views

urlpatterns = [
    # views.faq - funcao no arquivo view.py
    url(r'^$', views.faq_page, name='faqs'),

    url(r'^all_questions', views.get_all_questions, name='get_all_questions'), 
]
