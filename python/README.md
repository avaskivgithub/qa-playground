# simple_app_with_tests
"Test App" written in Python and with system tests [see the definition here](http://softwaretestingfundamentals.com/system-testing/#:~:text=SYSTEM%20TESTING%20is%20a%20level,compliance%20with%20the%20specified%20requirements.)

## Prerequisites 
You'll need:
* Sqlite
```
# on Windows you can run
> choco install sqlite
```
* Python 3. Originally "Test App" was created with Python 2 [see "READMEoriginal" for details](simple_app_with_tests/READMEoriginal).
```
# on Windows it was tested with
> python --version
Python 3.7.0
```

## Setup
* install all required python packages by running from the python\simple_app_with_tests\project directory
```
# from the root repo directory
> cd python\simple_app_with_tests\project
python\simple_app_with_tests\project> python setup.py develop
```
* setup test sqlite db by running
```
# from the root repo directory
> cd python\simple_app_with_tests\project\app
python\simple_app_with_tests\project> python db.py
```
* start REST api by running following command
```
# from the root repo directory
> cd python\simple_app_with_tests\project\app
python\simple_app_with_tests\project> python api_server.py
```
* start GUI (graphical user interface) by running following command
```
# from the root repo directory
> cd python\simple_app_with_tests\project\app
python\simple_app_with_tests\project> python web_gui.py
```

Note that venv is a better option for setup https://cheatography.com/ilyes64/cheat-sheets/python-virtual-environments/
```
pip install virtualenv
pip install virtualenvwrapper-win

python -m venv myvenv1
.\myvenv1\Scripts\activate
```

### Test
When api and GUI were started you can manually try them and run automated system tests example.

#### REST Api
Following examples are for Poweshell (for bash examples with curl see doc strings in the [api_server.py](simple_app_with_tests/project/app/api_server.py) )
```
# get all
> (Invoke-WebRequest 'http://127.0.0.1:12345/getall').Content | convertfrom-json | convertto-json -depth 100
{
    "Results":  [
                    {
                        "Id":  "T1",
                        "Name":  "T1 summary",
                        "Res":  -1,
                        "Error":  null
                    }
                ]
}

# add new test result
$json = '{"Res": 1, "Description": null, "Error": null, "Id": 111, "Name": "Test111"}'
Invoke-RestMethod 'http://127.0.0.1:12345/add' -Method Post -Body $json -ContentType 'application/json'
```

#### GUI
Just open in your browser http://localhost:5000/ 

### Automated System Tests
Ran the example of system tests
```
qa-playground\python\simple_app_with_tests\project> pytest -q .\tests\tests\api\test_api.py
qa-playground\python\simple_app_with_tests\project> pytest -q .\tests\tests\wui\test_wui.py
```

* For load tests need to install gnuplot on Windows and refactor hardcoded tmp dir in the draw_gnuplot function
http://spiff.rit.edu/classes/ast601/gnuplot/install_windows.html

# Tasks
Possible questions for a newcomer:
* Look for "Test App" issues
* Create a test design for "Test App" 
* What risks do you see in the sugested design of the "Test App"
* Fix tests for GUI. See stack trace from running
```
# from the root repo directory
> cd python\simple_app_with_tests
python\simple_app_with_tests> nosetests --ignore-file="test_.*load.*.py" -v project/tests/tests/
```
* Fix load tests. See stack trace from running
```
# from the root repo directory
> cd python\simple_app_with_tests
python\simple_app_with_tests> nosetests -v project/tests/tests/
```
* Extend the functionality of the "Test App" by adding one more feature
* Extend the test base

# Details
For details about "Test App":
* [see original "READMEoriginal" created for Python 2](simple_app_with_tests/READMEoriginal)
* [see app's structure documentation](simple_app_with_tests/docs/app)
* [see app's backlog](simple_app_with_tests/docs/backlog) and [1st sprint](simple_app_with_tests/docs/sprint1) plain text data (in real world you'll use some bug and issue tracker for this)
* [see app's code base](simple_app_with_tests/project/app)
* [see app's system tests](simple_app_with_tests/project/tests) (in real world you'll also have unit and integration tests)
