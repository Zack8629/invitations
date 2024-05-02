import random
import string
from urllib.parse import urljoin

import validators

from app import ShortLink


class LinkShortener:
    def __init__(self, _base_url, _short_base_url):
        self._base_url = _base_url
        self._short_base_url = _short_base_url
        self._symbols = string.ascii_lowercase + string.digits
        self._length_url = 1

    def get_orig_url(self, hash_event, hash_guest):
        return urljoin(self._base_url, f'{hash_event}/{hash_guest}')

    def generate_short_url(self, original_url):
        if not validators.url(original_url):
            return 'Некорректный URL'

        while True:
            new_short_url = urljoin(self._short_base_url, self._generate_random_code())
            existing_url = ShortLink.query.filter_by(short_url=new_short_url).first()
            if not existing_url:
                return new_short_url

            elif ShortLink.query.count() >= (len(self._symbols) ** self._length_url):
                self._length_url += 1

    def _generate_random_code(self):
        return ''.join(random.choice(self._symbols) for _ in range(self._length_url))

    def redirect(self, short_url):
        full_short_url = f'{self._short_base_url}/{short_url}'
        link = ShortLink.query.filter_by(short_url=full_short_url).first()
        return link.original_url if link else None


class LinkShortenerLocal:
    def __init__(self, _base_url, _short_base_url):
        self._base_url = _base_url
        self._short_base_url = _short_base_url
        self._symbols = string.ascii_lowercase + string.digits
        self._length_url = 1
        self._url_mapping = {}

    def get_orig_url(self, hash_event, hash_guest):
        return urljoin(self._base_url, f'{hash_event}/{hash_guest}')

    def generate_short_url(self, original_url):
        if not validators.url(original_url):
            return 'Некорректный URL'

        while True:
            new_short_url = urljoin(self._short_base_url, self._generate_random_code())
            if new_short_url not in self._url_mapping:
                self._url_mapping[new_short_url] = original_url
                return new_short_url

            elif len(self._url_mapping) >= (len(self._symbols) ** self._length_url):
                self._length_url += 1

    def _generate_random_code(self):
        return ''.join(random.choice(self._symbols) for _ in range(self._length_url))

    def redirect(self, short_url):
        original_url = self._url_mapping.get(short_url)
        return original_url or 'Ссылка не найдена'
