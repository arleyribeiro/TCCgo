from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', views.rules_list, name='rules_list'), # List all the rules of the user

    # login required ->
    # Ajax requests urls
    url(r'^all_rules', login_required(views.get_all_rules), name='get_all_rules'), # Get all user rules
    url(r'^all_type', login_required(views.get_all_types), name='get_all_types'), # Get all rules types existent
    url(r'^create_rule', login_required(views.create_rule), name='create_rule'), # Create a new rule from a post form
    url(r'^verify_name', login_required(views.verify_name), name='verify_name'), # Verify if a given name already exists in database
    url(r'^delete_rule', login_required(views.delete_rule), name='delete_rule'), # Delete a rule passed in the request
    url(r'^filter_rules', login_required(views.filter_rules), name='filter_rules'), # Return a filtered set of rules
    url(r'^update_rule', login_required(views.update_rule), name='update_rule'), # Update a rule with the send data

    # public urls


]
