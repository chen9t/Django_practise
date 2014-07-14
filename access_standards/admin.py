#encoding=utf-8
from access_standards.models import AccessStandard
from django.contrib import admin


class AccessStandardAdmin(admin.ModelAdmin):
    list_display = ('city', 'emission_standard', 'standard_details', 'DVM')
    search_fields = ['city']
    ordering = ('id', )

admin.site.register(AccessStandard, AccessStandardAdmin)
