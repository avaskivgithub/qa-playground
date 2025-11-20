Very simple example of calling /api/users from https://reqres.in/api-docs/ based on https://robotframework.org/RobotDemo/

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
robot keyword_driven.robot
robot gherkin.robot
```
### Clean up generated files
```
inv remove-docs
inv clean
```