*** Settings ***
Documentation     Example test cases using the keyword-driven testing approach.
...
...               All tests contain a workflow constructed from keywords in
...               ``RequestLibrary.py``. 
Library           RequestLibrary.py

*** Test Cases ***
Simple GET
    Call get    /api/users
    Result code should be    200
