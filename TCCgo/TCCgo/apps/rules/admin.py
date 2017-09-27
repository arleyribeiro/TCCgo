from django.contrib import admin

from .models import Rule, RuleType, Inconsistency, InconsistencyType
# 
# class RuleTypeAdmin(admin.ModelAdmin):
#     list_display = ['pattern', 'warning', 'name', 'weight', 'date']
#
# class RuleAdmin(admin.ModelAdmin):
#     list_display = ['type']
#
# class InconsistencyAdmin(admin.ModelAdmin):
#     list_display = []
#
# class InconsistencyTypeAdmin(admin.ModelAdmin):
#     list_display = ['type']
#
#
# admin.site.register(RuleType, RuleTypeAdmin)
# admin.site.register(Rule, RuleAdmin)
# admin.site.register(InconsistencyType, InconsistencyTypeAdmin)
# admin.site.register(Inconsistency, InconsistencyAdmin)
