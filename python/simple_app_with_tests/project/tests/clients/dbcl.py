#!/usr/bin/python

from app.db import SqliteClient

class TestDBClient(SqliteClient):

    def __init__(self, dbs_dir='sqlite_dbs', db_name='test.db'):

        super(TestDBClient, self).__init__(dbs_dir, db_name)

    def get_all(self):

        return self.get_all_resultrs_records()

    def get_record_by_id(self, test_id):

        record = self.get_results_record_by_id(test_id)
        return record

    def delete_all_records(self):

        sql = "DELETE FROM {}".format(self.table_results)
        print(sql)
        self._execute_statement(sql)
        self.connection.commit()

if __name__ == '__main__':

    cl = TestDBClient()

    cl.open_connection()
    print(cl.get_all())
    cl.close_connection()
