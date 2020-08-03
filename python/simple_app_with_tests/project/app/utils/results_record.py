#!/usr/bin/env python
import logging
from app.db import SqliteClient

"""
Wrapper for record from Results table. Class ResultsRecord:

    Expected input parameters:
        args: (id, name, descr, res, error_desc)
        or
        kwargs: (record_in_db_format = {"Res": 1, "Description": Null, "Error": Null, "Id": 3, "Name": "Test3"})

    Enforced fields limitations:
        id = NotEmpty('id') # id can't be empty
        name = NotEmptyString('name') # name string can't be empty
        res = Result('res') # res should be in [-1, 0, 1] range and for wui ['Not Started', 'Failed', 'Passed']

Based on recipe: http://chimera.labs.oreilly.com/books/1230000000393/ch08.html#datamodel
"""

error_def = 2
_db_res_representation = {'Not Started': -1,
                          'Failed': 0,
                          'Passed': 1,
                          'Error': error_def}

# Class to which we'll delegate converting from db representation to wui and back
class Formater(object):

    def __init__(self, id, name, descr, res, error_desc):

        self.id = id
        self.name = name
        self.descr = descr
        self.res = res
        self.error_desc = error_desc

        self._db_res_wui = {_db_res_representation[key]: key for key in _db_res_representation.keys()}

    def get_db_format(self):

        table_results_column_values = [self.id, self.name, self.descr, self.res, self.error_desc]

        row = {}
        for clmn_name, value in zip(SqliteClient.table_results_column_names, table_results_column_values):
            row[clmn_name] = value

        return row

    def get_wui_format(self):

        row = self.get_db_format()
        try:
            row['Res'] = self._db_res_wui[row['Res']]
        except:
            row['Res'] = self._db_res_wui[error_def]

        return row


# Descriptor to set a value
class Descriptor(object):

    def __init__(self, name=None, **opts):

        logging.basicConfig(level=logging.DEBUG)

        self.name = name
        for key, value in opts.items():
            setattr(self, key, value)

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value

# Descriptor for enforcing types
class Typed(Descriptor):
    expected_types = [type(None)]

    def __set__(self, instance, value):

        if type(value) not in self.expected_types:
            msg = 'Type Error: "{}" expected one of the {} but received {}'.format(self.name, str(self.expected_types), str(type(value)))
            logging.error(msg)
            raise TypeError(msg)
        super(Typed, self).__set__(instance, value)

# Descriptor for filtering res values
class Result(Descriptor):

    def __set__(self, instance, value):

        valid_values = [val for val in _db_res_representation.values() if val != error_def]

        if value in _db_res_representation.keys():
            value = _db_res_representation[value]
        elif value not in valid_values:
            value = _db_res_representation['Error']

        super(Result, self).__set__(instance, value)

class NotEmpty(Descriptor):

    def __set__(self, instance, value):
        if not value:
            msg = 'Value Error: "{}" can not be empty'.format(self.name)
            logging.error(msg)
            raise ValueError(msg)
        super(NotEmpty, self).__set__(instance, value)

class String(Typed):
    # python 2
    # expected_types = [str, unicode]
    # python 3
    # https://stackoverflow.com/questions/19877306/nameerror-global-name-unicode-is-not-defined-in-python-3
    expected_types = [bytes, str]


class NotEmptyString(String, NotEmpty):
    pass

class ResultsRecord(object):

    id = NotEmpty('id')
    name = NotEmptyString('name')
    res = Result('res')

    def __init__(self, *args, **kwargs):
        """
        Expected input parameters:
            args: (id, name, descr, res, error_desc)
            or
            kwargs: (record_in_db_format = {"Res": 1, "Description": Null, "Error": Null, "Id": 3, "Name": "Test3"})
        """

        try:
            id, name, descr, res, error_desc = args
        except:
            # When instance is initiated with dict from app.db.SqliteClient.get_results_record_by_id
            try:
                db_record = kwargs['record_in_db_format']
                id, name, descr, res, error_desc = [db_record[key] for key in SqliteClient.table_results_column_names]
            except:
                msg = 'Type Error: "{}" incorrect initialization'.format(self.__class__.__name__)
                logging.error(msg)
                raise TypeError(msg)

        self.id = id
        self.name = name
        self.descr = descr
        self.res = res
        self.error_desc = error_desc

        self.formater = Formater(self.id, self.name, self.descr, self.res, self.error_desc)

    def get_dict(self):
        """Map attributes (id, name, etc.) to column names.
        :return Dictionary like:
             |                     {
             |                         "Description": "Test steps",
             |                         "Error": "Failed with unexpected result",
             |                         "Id": 2,
             |                         "Name": "Test2",
             |                         "Res": 0
             |                     }
        """

        return self.formater.get_db_format()

    def get_dict_for_wui(self):
        """Convert integer Result value into string (Passed, Failed, etc.) for wui.
        :return Dictionary like:
             |                     {
             |                         "Description": "Test steps",
             |                         "Error": "Failed with unexpected result",
             |                         "Id": 2,
             |                         "Name": "Test2",
             |                         "Res": Failed
             |                     }
        """

        return self.formater.get_wui_format()


if __name__ == '__main__':

    print(ResultsRecord(1, 'Test', '', 'Failed', '').get_dict())
