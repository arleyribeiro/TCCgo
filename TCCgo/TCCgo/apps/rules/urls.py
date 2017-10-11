from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.rules_list, name='rules_list'), # List all the rules of the user

    # Ajax requests urls
    url(r'^all_rules', views.get_all_rules, name='get_all_rules'), # Get all user rules
    url(r'^all_type', views.get_all_types, name='get_all_types'), # Get all rules types existent
    url(r'^create_rule', views.create_rule, name='create_rule'), # Create a new rule from a post form
    url(r'^verify_name', views.verify_name, name='verify_name'), # Verify if a given name already exists in database
    url(r'^delete_rule', views.delete_rule, name='delete_rule'), # Delete a rule passed in the request
    url(r'^filter_rules', views.filter_rules, name='filter_rules'), # Return a filtered set of rules
    url(r'^update_rule', views.update_rule, name='update_rule'), # Update a rule with the send data
]
