# -*- coding: utf-8 -*-

from django.db import models


class ShortURLMap(models.Model):
    ''' Record short url map.'''

    code = models.CharField(
        max_length=60,
        db_index=True,
        unique=True,
        verbose_name=u'长url的MD5码')
    url_long = models.URLField(max_length=500, verbose_name=u'实际url')
    url_short = models.CharField(
        max_length=50,
        db_index=True,
        verbose_name=u'短url')
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    clicks = models.IntegerField(max_length=11, verbose_name=u'点击次数')

    class Meta:
        db_table = 'short_url_map'
        ordering = ['created_on', ]
        verbose_name = u'短链接映射表'
        verbose_name_plural = u'短链接映射表'

    def short_url_link(self):
        url_link = self.url_short
        return u'<a href="/%s" target="_blank">%s</a>' % (url_link, url_link)
    short_url_link.allow_tags = True
    short_url_link.short_description = u'短链接'

    def long_url_link(self):
        return '<a href="%s" target="_blank">%s</a>' % (self.url_long, self.url_long)
    long_url_link.allow_tags = True
    long_url_link.short_description = u'实际链接'
