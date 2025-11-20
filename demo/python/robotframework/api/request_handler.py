import requests

class RequestHandler(object):
    HEADERS = {'x-api-key': 'reqres-free-v1'}

    def __init__(self):
        self._base_url = 'https://reqres.in'
        self._response = ''

    def call(self, http_method='get', uri='/api/users', params=None):

        url = self._base_url + uri
        try:
            if http_method.lower() == 'get':
                self._response = requests.get(url, headers=self.HEADERS, params=params)
        except Exception as error:
            raise RequestError('{}: {}'.format(type(error), error))
        return (self._response.status_code, self._response.text)

class RequestError(Exception):
    pass
