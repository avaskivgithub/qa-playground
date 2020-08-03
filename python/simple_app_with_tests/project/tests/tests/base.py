import unittest
from tests.clients.apicl import TestRestApiClient
from tests.clients.dbcl import TestDBClient


class Base(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        cls.api = TestRestApiClient()
        cls.db = TestDBClient()
        cls.db.open_connection()

        cls.wui = TestRestApiClient(port=5000)

    @classmethod
    def tearDownClass(cls):

        cls.db.close_connection()

    def setUp(self):

        self.db.delete_all_records()

    def add_record(self, id, name, descr=None, res=-1, error_desc=None):

        self.db.add_results_record(id, name, descr, res, error_desc)

