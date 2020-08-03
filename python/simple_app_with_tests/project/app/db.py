#!/usr/bin/python
# -*- coding: utf-8 -*-

# Based on example: http://zetcode.com/db/sqlitepythontutorial/

import sqlite3 as lite
import os
import logging
from inspect import signature, getargspec

con = None
root_dir = 'sqlite_dbs'

class SqliteClient(object):

    table_results_name_to_type = [('Id', 'TEXT'),
                                  ('Name', 'TEXT'),
                                  ('Description', 'BLOB'),
                                  ('Res', 'INT'),
                                  ('Error', 'BLOB')]
    table_results_column_names = [el[0] for el in table_results_name_to_type]

    def __init__(self, dbs_dir='sqlite_dbs', db_name='test.db'):

        logging.basicConfig(level=logging.DEBUG)

        self.dbs_dir = os.path.join(os.path.dirname(__file__), dbs_dir)
        self.db_name = db_name
        self.db_file_path = os.path.join(self.dbs_dir, self.db_name)

        self.connection = None

        self.table_results = 'Results'
        self.column_id = 'Id'
        self.column_res = 'Res'

    # ===> Open / Close connection and ability to use context manager

    def open_connection(self, db_path=None):

        if db_path is None:
            db_path = self.db_file_path

        try:
            os.mkdir(self.dbs_dir)
        except:
            pass

        if self.connection is None:
            self.connection = lite.connect(db_path)

    def close_connection(self):

        try:
            self.connection.close()
        except:
            pass

    def __enter__(self):

        self.open_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.close_connection()
        self.connection = None

    # ===> Open / Close cursor and executing statement

    def _execute_statement(self, sql_statement, *args):

        data = None

        curs = self.connection.cursor()
        logging.info(sql_statement)

        try:
            curs.execute(sql_statement, *args)
            data = curs.fetchall()
        except Exception as e:
            logging.warning(e)
        finally:
            curs.close()

        return data

    # ===> Methods for select / insert etc.

    def get_version(self):

        return self._execute_statement('SELECT SQLITE_VERSION()')

    def get_all_resultrs_records(self):
        """Returns all records from Results table:
             |                  {
             |                      "Results": [
             |                          {
             |                              "Description": null,
             |                              "Error": null,
             |                              "Id": 1,
             |                              "Name": "Test1",
             |                              "Res": 1
             |                          },
             |                          {
             |                              "Description": "Test steps: \n1. Step1",
             |                              "Error": "Failed with unexpected result",
             |                              "Id": 2,
             |                              "Name": "Test2",
             |                              "Res": 0
             |                          }
             |                      ]
             |                  }
        """

        raw_data = self._execute_statement('SELECT * FROM ' + self.table_results)

        data = {'Results': []}
        try:
            for row in raw_data:
                next_row = {}
                for clmn_name, value in zip(self.table_results_column_names, row):
                    next_row[clmn_name] = value
                data['Results'].append(next_row)
        except:
            pass

        return data

    def get_results_record_by_id(self, id):
        """Returns record from Results table by Id:
             |                     {
             |                         "Description": "Test steps: \n1. Step1",
             |                         "Error": "Failed with unexpected result",
             |                         "Id": 2,
             |                         "Name": "Test2",
             |                         "Res": 0
             |                     }
        """
        sql = "SELECT * FROM {} WHERE {} = ?".format(self.table_results, self.column_id,)
        result = self._execute_statement(sql, (id,))

        row = {}

        if result:
            id, name, descr, res, error_desc = result[0]

            for clmn_name, value in zip(self.table_results_column_names, [id, name, descr, res, error_desc]):
                row[clmn_name] = value

        return row

    def get_count_resultrs_records(self, res=1):

        try:
            count = self._execute_statement('SELECT count(*) '
                                            'FROM {} '
                                            'WHERE {} = {}'.format(self.table_results,
                                                                   self.column_res,
                                                                   res))[0][0]
        except:
            count = 0

        return count

    def add_results_record(self, id, name, descr=None,
                           res=-1, error_desc=None):
        """
        Params:
        res: -1 - Not Started
              1 - Passed
              0 - Failed
            any other value - Error
        """
        values = (id, name, descr, res, error_desc)

        sql = "DELETE FROM {} WHERE {} = ?".format(self.table_results, self.column_id,)
        self._execute_statement(sql, (id,))

        sql = "INSERT INTO {} VALUES({})".format(self.table_results,
                                                 ', '.join(len(values) * ['?']))

        self._execute_statement(sql, values)
        self.connection.commit()

    @classmethod
    def _get_params_names_for_add_results_record(self):

        # https://stackoverflow.com/questions/990016/how-to-find-out-the-arity-of-a-method-in-python
        # co_argcount = self.add_results_record.func_code.co_argcount
        co_argcount = len(getargspec(self.add_results_record))

        # return self.add_results_record.func_code.co_varnames[1:co_argcount]
        print(getargspec(self.add_results_record).args)
        return getargspec(self.add_results_record).args[1:co_argcount]

    # ==>> Methods for Create / Delete table
    def create_table_results(self):

        fields = ['{} {}'.format(el[0], el[1])
                  for el in self.table_results_name_to_type]

        sql = "CREATE TABLE {}({})".format(self.table_results,
                                           ', '.join(fields))

        self._execute_statement(sql)

    def delete_table_results(self):

        sql = "DROP TABLE {}".format(self.table_results)

        self._execute_statement(sql)


if __name__ == '__main__':

    # cl = SqliteClient()
    # cl.open_connection()
    # print cl.get_version()
    # cl.close_connection()

    # print SqliteClient._get_params_names_for_add_results_record()

    with SqliteClient() as cl:
        # print cl.get_version()

        cl.create_table_results()
        # add and update
        # cl.add_results_record(id=1, name='Test1', res=-1)
        # cl.add_results_record(id=1, name='Test1', res=1)
        # add with all fields
        cl.add_results_record(id=2, name='Test2', descr='Test steps: 1. Step1',
                              res=0, error_desc='Failed with unexpected result')

        print(cl.get_all_resultrs_records())
        print(cl.get_results_record_by_id(2))
        # print cl.get_count_resultrs_records()

# EOF