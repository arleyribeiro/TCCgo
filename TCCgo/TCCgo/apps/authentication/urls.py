from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # URL DE TESTE
    # login required ->
    url(r'^register/change_password', login_required(views.change_password), name='change_password'),
    url(r'^register/update_user', login_required(views.update_user), name='update_user'),
    url(r'^register/delete_user', login_required(views.delete_user), name='delete_user'),
    url(r'^password/$', login_required(views.password), name='password'),

    # public urls
    url(r'^register/$', views.register, name='register'),
    url(r'^register/create_user', views.create_user, name='create_user'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^get_logged_user', views.get_logged_user, name='get_logged_user'),
    url(r'^check_unique_email', views.check_unique_email, name='check_unique_email'),
    url(r'^check_login', views.check_login, name='check_login'),
]
