from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.rules_list, name='rules_list'), # List all the rules of the user

    url(r'^all_rules', views.get_all_rules, name='get_all_rules'), # TESTE
]
