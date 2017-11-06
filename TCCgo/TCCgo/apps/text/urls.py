from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # URL DE TESTE

    url(r'^submit_page', login_required(views.text_page), name='submit_page'), # page: submit text
    url(r'^submit', login_required(views.create_text), name='submit'), # create text, action of submit (post)
    url(r'^all_texts', login_required(views.get_all_texts), name='all_texts'), # return get all texts (get)
    url(r'^list_texts', login_required(views.all_texts_page), name='list_texts'), # page: list all texts
    url(r'^filter_texts', login_required(views.filter_texts), name='filter_texts'), # return a filtered set of rules (get)
    url(r'^delete_text', login_required(views.delete_text), name='delete_text'), # delete text (post / ajax)
    url(r'^edit_text/', login_required(views.edit_text_page), name='edit_text'),
    url(r'^update_text', login_required(views.update_text), name='update_text'),
    url(r'^get_text', login_required(views.get_text), name='get_text'),
    url(r'^processing_text', login_required(views.processing_text_page), name='processing_text'),
    url(r'^get_processed_text', login_required(views.get_processed_text), name='get_processed_text'),
]
