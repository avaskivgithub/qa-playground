#!/usr/bin/python

from app.utils.rest_client import RestApiBasicClient

class TestRestApiClient(RestApiBasicClient):

    def __init__(self,
                 hostname='127.0.0.1',
                 port=12345):

        super(TestRestApiClient, self).__init__(hostname, port)

    def add(self, id, name, descr=None,
                  res=-1, error_desc=None):

        record = {'Id': id,
                  'Name': name,
                  'Description': descr,
                  'Res': res,
                  'Error': error_desc}

        return self._post('/add', record)

    def get_all(self):

        return self._get('/getall')

    def delete_results(self):

        return self._get('/clear')

    def setup_results(self):

        return self._get('/setup')

if __name__ == '__main__':

    cl = TestRestApiClient()
    print(cl.get_all().json())
