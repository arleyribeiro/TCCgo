from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # URL DE TESTE
    url(r'^register/$', views.register, name='register'),
    url(r'^register/create_user', views.create_user, name='create_user'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^get_logged_user', views.get_logged_user, name='get_logged_user'),
    url(r'^register/update_user', views.update_user, name='update_user'),
]
