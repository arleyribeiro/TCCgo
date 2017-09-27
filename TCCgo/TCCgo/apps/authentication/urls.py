from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # URL DE TESTE
    url(r'^register/$', views.register, name='register'),
    url(r'^register/create_user', views.create_user, name='create_user'),
]
