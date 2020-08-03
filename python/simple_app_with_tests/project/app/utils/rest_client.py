#!/usr/bin/python

import requests
import json

class RestApiBasicClient(object):

    def __init__(self,
                 hostname='127.0.0.1',
                 port=12345):

        self.hostname = hostname
        self.port = port

        self.base_url = 'http://{}:{}'.format(self.hostname, self.port)

    def _post(self, url, data):

        uri = self.base_url + url
        return requests.post(uri, json=data)

    def _get(self, url, params=None):

        uri = self.base_url + url
        return requests.get(uri, params=params)

# EOF