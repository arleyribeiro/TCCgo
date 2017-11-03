from django.contrib import admin

from .models import *

class RuleAdmin(admin.ModelAdmin):
    list_display = ['pattern', 'warning', 'name', 'date', 'scope']

class RuleTypeAdmin(admin.ModelAdmin):
    list_display = ['type']

class InconsistencyAdmin(admin.ModelAdmin):
    list_display = ['id']

class InconsistencyTypeAdmin(admin.ModelAdmin):
    list_display = ['type']


admin.site.register(RuleType, RuleTypeAdmin)
admin.site.register(Rule, RuleAdmin)
admin.site.register(InconsistencyType, InconsistencyTypeAdmin)
admin.site.register(Inconsistency, InconsistencyAdmin)
