#!/usr/bin/env python

class PageIndex(object):

    uri = '/'

    class Buttons(object):

        add = {'name': 'addTest'}
        delete = {'name': 'deleteAllTests'}

    class Tables(object):

        allresults = {'name': 'allTestsTable', 'id': 'allTestsTable'}

    class Links(object):

        home = {'link_text': 'Home'}
        add = {'link_text': 'Add Test'}

class PageAdd(object):

    uri = '/showAdd'

    class Inputs(object):

        test_id = {'name': 'inputId', 'id': 'inputId'}
        test_name = {'name': 'inputName', 'id': 'inputName'}
        test_res = {'name': 'inputRes', 'id': 'inputRes'}

    class TextAreas(object):

        description = {'name': 'areaDescription'}
        error = {'name': 'areaError'}

    class Buttons(object):

        add = {'name': 'btnAdd', 'id': 'btnAdd'}
        cancel = {'name': 'btnCancel', 'id': 'btnCancel'}

class PageEdit(object):

    uri = '/edit/{}'


if __name__ == '__main__':

    pg_index = PageIndex
    print(pg_index.uri)

    print(pg_index.Buttons.add['name'])