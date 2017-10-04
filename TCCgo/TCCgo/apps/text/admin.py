from django.contrib import admin

from .models import *

class TextAdmin(admin.ModelAdmin):
    list_display = ['content', 'title', 'user']

class FragmentAdmin(admin.ModelAdmin):
    list_display = ['content', 'position', 'text']

admin.site.register(Text, TextAdmin)
admin.site.register(Fragment, FragmentAdmin)
