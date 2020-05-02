import json
import os
import requests
import time


class API(object):

    def __init__(self, secret='', key=''):
        self.url = 'https://api.kraken.com/0/'
        self.session = requests.Session()
        self.response = None
        self.call_rate_limit = 15
        self.

    def public(self, method='Time', input=None, headers=None, timeout=None):
        url = self.url + 'public/' + method

        if not input:
            input = {}
        if not headers:
            headers = {}

        self.response = self.session.post(url, data=input, headers=headers, timeout=timeout)

        if self.response.ok is False:
            self.response.raise_for_status()

        return self.response.json()

    def private(self, method, input=None, headers=None, timeout=None):
    url = self.url + 'private/' + method

    if not input:
        input = {}
    if not headers:
        headers = {}

    self.response = self.session.post(url, data=input, headers=headers, timeout=timeout)

    if self.response.ok is False:
        self.response.raise_for_status()

    return self.response.json()

