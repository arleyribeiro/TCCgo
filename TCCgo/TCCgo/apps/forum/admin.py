from django.contrib import admin

from .models import *

class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'message', 'date', 'user']

class PostAdmin(admin.ModelAdmin):
    list_display = ['body', 'index', 'date', 'reply', 'topic']

admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
