#!/usr/bin/python

# Based on example: http://code.tutsplus.com/tutorials/creating-a-web-app-from-scratch-using-python-flask-and-mysql--cms-22972

from flask import Flask, render_template, request, redirect, url_for
from app.utils.results_record import ResultsRecord
from api_client import RestApiClient

app = Flask(__name__)
api_cl = RestApiClient()

def _get_all_tests():
    """Returns list of tests:
                        [
                            {
                                "Description": null,
                                "Error": null,
                                "Id": 1,
                                "Name": "Test1",
                                "Res": 1
                            },
                            {
                                "Description": "Test steps: \\n1. Step1",
                                "Error": "Failed with unexpected result",
                                "Id": 2,
                                "Name": "Test2",
                                "Res": 0
                            }
                        ]
    """

    all_tests = api_cl.get_all()['Results']

    all_tests_converted = []
    for row in all_tests:
        all_tests_converted.append(ResultsRecord(record_in_db_format=row).get_dict_for_wui())

    return all_tests_converted

def _get_test(test_id):

    test_data = api_cl.get_record_by_id(test_id)

    return test_data

@app.route('/showAdd')
def showAdd():

    return render_template('add.html')

@app.route('/edit/<testid>')
def edit(testid):

    test_data = _get_test(testid)
    record = ResultsRecord(record_in_db_format=test_data).get_dict_for_wui()

    return render_template('edit.html', result=record)

@app.route('/add', methods=['POST'])
def add():

    # read the posted values from the UI
    _id = request.form['inputId']
    _name = request.form['inputName']
    _desc = request.form['areaDescription']
    _res = request.form['inputRes']
    _error_desc = request.form['areaError']

    api_cl.add(id=_id, name=_name, descr=_desc, res=_res, error_desc=_error_desc)
    return redirect(url_for('main'))

@app.route('/reset')
def deleteAll():

    api_cl.reset_data()
    return redirect(url_for('main'))

@app.route('/')
def main():

    all_tests = _get_all_tests()
    return render_template('index.html', result=all_tests)

if __name__ == "__main__":

    app.run(host='0.0.0.0')  # listen on all network interfaces
