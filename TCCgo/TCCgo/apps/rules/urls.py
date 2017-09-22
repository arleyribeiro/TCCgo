from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.rules_list, name='rules_list'), # List all the rules of the user
]
