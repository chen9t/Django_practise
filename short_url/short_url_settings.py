# -*- coding: utf-8 -*-

from django.conf import settings

SHORT_URL_LENGTH = getattr(settings, 'SHORT_URL_LENGTH', 6)
DOMAIN_NAME = getattr(settings, 'DOMAIN_NAME', 'http://127.0.0.1:8000/')
