# -*- coding: utf-8 -*-

from django.contrib import admin

from short_url.models import ShortURLMap


class ShortURLMapAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_url_link', 'long_url_link', 'created_on', 'clicks')
    search_fields = ['url', 'url_short']
    date_hierarchy = 'created_on'

admin.site.register(ShortURLMap, ShortURLMapAdmin)