import requests
import time

import urllib.parse
import hashlib
import hmac
import base64


class API(object):

    def __init__(self, secret='', key=''):
        self.url = 'https://api.kraken.com/0/'
        self.session = requests.Session()
        self.response = None
        self.call_rate_limit = 15

    def public(self, method='Time', input=None, timeout=None):
        url = self.url + 'public/' + method

        if not input:
            input = {}

        self.response = self.session.post(url, data=input, timeout=timeout)

        if self.response.ok is False:
            self.response.raise_for_status()

        return self.response.json()

    def private(self, method, input=None, timeout=None):
        url = self.url + 'private/' + method

        if not input:
            input = {}

        input['nonce'] = self._nonce()
        headers = {
            'API-Key': self.key,
            'API-Sign': self._sign(input, '/0/private/' + method)
        }
        self.response = self.session.post(url, data=input, headers=headers, timeout=timeout)

        if self.response.ok is False:
            self.response.raise_for_status()

        return self.response.json()

    def load_key(self, path):
        with open(path, 'r') as f:
            self.key = f.readline().strip()
            self.secret = f.readline().strip()
        return

    def _nonce(self):
        return int(1000*time.time())

    def _sign(self, input, urlpath):
        postdata = urllib.parse.urlencode(input)
        encoded = (str(input['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()

        signature = hmac.new(base64.b64decode(self.secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(signature.digest())
      
        return sigdigest.decode()

    