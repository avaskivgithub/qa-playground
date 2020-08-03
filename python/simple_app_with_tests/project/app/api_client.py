#!/usr/bin/python

from utils.rest_client import RestApiBasicClient
from utils.results_record import ResultsRecord
import logging

class RestApiClient(RestApiBasicClient):

    def __init__(self,
                 hostname='127.0.0.1',
                 port=12345):

        logging.basicConfig(level=logging.DEBUG)
        super(RestApiClient, self).__init__(hostname, port)

    def add(self, id, name, descr=None,
                  res=-1, error_desc=None):

        record = ResultsRecord(id, name, descr, res, error_desc).get_dict()
        logging.info('Calling /add with {}'.format(record))
        return self._post('/add', record)

    def get_all(self):

        logging.info('Calling /getall')
        return self._get('/getall').json()

    def get_record_by_id(self, id):

        logging.info('Calling /getrecord')
        return self._get('/getrecord', params={'id': id}).json()

    def reset_data(self):

        logging.info('Calling reset data')

        self._get('/clear')
        self._get('/setup')

if __name__ == '__main__':

    cl = RestApiClient()

    print(cl.get_all())
    cl.add(id=7, name='T7', descr='somedescription')
    print(cl.get_record_by_id(id='T7'))
