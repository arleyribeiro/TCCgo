from django.conf.urls import url
from . import views
urlpatterns = [
    # views.faq - funcao no arquivo view.py
    url(r'^$', views.faq_page, name='faqs'),
]
