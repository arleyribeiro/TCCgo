from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.text_page, name='text_page'),
    url(r'^submit_page', views.text_page, name='submit_page'),
    url(r'^submit', views.submit_text, name='submit'),
]
