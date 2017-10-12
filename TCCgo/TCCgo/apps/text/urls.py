from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # URL DE TESTE
    url(r'^submit_page', views.text_page, name='submit_page'), # page: submit text
    url(r'^submit', views.create_text, name='submit'), # create text, action of submit (post)
    url(r'^all_texts', views.get_all_texts, name='all_texts'), # return get all texts (get)
    url(r'^list_texts', views.all_texts_page, name='list_texts'), # page: list all texts
    url(r'^filter_texts', views.filter_texts, name='filter_texts'), # return a filtered set of rules (get)
]
