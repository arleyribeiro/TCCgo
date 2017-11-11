from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', login_required(views.forum_page), name='forum'),
    url(r'^new_topic',login_required(views.new_topic), name='new_topic'),
    url(r'^create_topic',login_required(views.create_topic), name='create_topic'),
    url(r'^filter_topics', login_required(views.filter_topics), name='filter_topics'),
    url(r'^view_topic', login_required(views.view_topic), name='view_topic'),
    url(r'^all_topics', login_required(views.get_all_topics), name='all_topics'),


]
