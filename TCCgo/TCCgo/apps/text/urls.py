from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # URL DE TESTE
    url(r'^submit_page', views.text_page, name='submit_page'),
    url(r'^submit', views.submit_text, name='submit'),
    url(r'^all_texts', views.get_all_texts, name='all_texts'),
    url(r'^list_texts', views.all_texts_page, name='list_texts'),
]
