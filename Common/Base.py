import os
import random
import requests
from requests import sessions


class Base:
    @classmethod
    def base_request(self, url, method='Get', **kwargs):
        with sessions.Session() as session:
            return session.request(method=method, url=url, **kwargs)

    def base_get(self, url, params=None, **kwargs):
        return requests.get(url, params=params, **kwargs)

    def base_post(self, url, data=None, json=None, **kwargs):
        return requests.post(url, data=data, json=json, **kwargs)
