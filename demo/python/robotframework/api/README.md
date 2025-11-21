# Overview
Very simple example of calling /api/users from https://reqres.in/api-docs/ based on https://robotframework.org/RobotDemo/
```
Test Case:
1. Call https://reqres.in/api/users
2. Check that response status code is 200
3. Check that response body contains "total":12
```

## Setup
```
pip install -r requirements.txt

# windows
Set-ExecutionPolicy Unrestricted -Scope Process
~\Documents\PyEnvs\RobotDemo\Scripts\Activate.ps1

invoke --list
```

## Run Tests
```
robot gherkin.robot
robot keyword_driven.robot
```
### Clean up generated files
```
inv remove-docs
inv clean
```