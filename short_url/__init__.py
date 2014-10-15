# -*- coding: utf-8 -*-
import hashlib

from short_url.models import ShortURLMap

from short_url.short_url_settings import SHORT_URL_LENGTH


CODE_MAP = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
    'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
    'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
    'y', 'z', '0', '1', '2', '3', '4', '5',
    '6', '7', '8', '9', 'A', 'B', 'C', 'D',
    'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z'
)


class ShortURL(object):
    ''' Generate short url according to long url, and get long url according to
    short url.

    usage:
    * get short url:
        s = ShortURL('/long/url/')
        s.get_short_url()
    * get long url:
        ShortURL.get_long_url('7YbNv')
    '''

    def __init__(self, url):
        self.url_long = url
        self.md = self.get_md5(url)

    def get_md5(self, s=None):
        if not s:
            s = self.url_long
        s = s.encode('utf8') if isinstance(s, unicode) else s
        m = hashlib.md5(s)
        return m.hexdigest()

    def _get_key_list(self, key_length):
        key_length = key_length - 1
        hkeys = []
        md = self.md
        for i in xrange(0, 4):
            n = int(md[i*8:(i+1)*8], 16)
            v = []
            e = 0
            for j in xrange(0, key_length):
                x = 0x0000003D & n
                e |= ((0x00000002 & n) >> 1) << j
                v.insert(0, CODE_MAP[x])
                n = n >> 6
            e |= n << 5
            v.insert(0, CODE_MAP[e & 0x0000003D])
            hkeys.append(''.join(v))
        return hkeys

    def get_short_url(self):
        url = ''
        surls = ShortURLMap.objects.filter(code=self.md)
        if surls.exists():
            url = surls[0].url_short
        else:
            key_list = self._get_key_list(SHORT_URL_LENGTH)
            for key in key_list:
                surls = ShortURLMap.objects.filter(url_short=key)
                if not surls.exists():
                    try:
                        ShortURLMap.objects.create(code=self.md, url_short=key,
                                url_long=self.url_long, clicks=0)
                    except:
                        surl = ShortURLMap.objects.get(code=self.md)
                        url = surl.url_short
                    else:
                        url = key
                    break

        return url

    @classmethod
    def get_long_url(cls, url_short):
        url = ''
        try:
            url_short = url_short.split('/')[-1]
            surl = ShortURLMap.objects.get(url_short=url_short)
        except ShortURLMap.DoesNotExist:
            pass
        else:
            url = surl.url_long
        return url

    @classmethod
    def get_clicks(cls, url_short):
        count = -1
        try:
            url_short = url_short.split('/')[-1]
            surl = ShortURLMap.objects.get(url_short=url_short)
        except ShortURLMap.DoesNotExist:
            pass
        else:
            count = surl.clicks
        return count
