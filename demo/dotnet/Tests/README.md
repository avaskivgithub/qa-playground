# Overview

## AUT - API
API being test is:
- https://reqres.in/signup - Free API Key
- https://reqres.in/api-docs/

## Run Tests
- To run tests
```
dotnet clean; dotnet test --logger "console;verbosity=detailed"
```
- To run tests with html results
```
dotnet clean; dotnet test --logger "html;logfilename=testResults.html"
```