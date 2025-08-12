# Overview

## AUT - API
API being used as an example for testing is:
- https://reqres.in/signup - Free API Key
- https://reqres.in/api-docs/

### Mock Test Api
Not to hit real test apis we can start local server just not to reach limit of the real test api.
- From Mocks\Api start local server
```
qa-playground\demo\dotnet\Mocks\Api> python -m http.server 8888
```
- For tests replace appsettings.test.json with appsettings.test_local.json
```
qa-playground\demo\dotnet\Tests> cp appsettings.test_local.json appsettings.test.json
```

## Run Tests
- To run tests
```
dotnet clean; dotnet test --logger "console;verbosity=detailed"
```
- To run tests with html results
```
dotnet clean; dotnet test --logger "html;logfilename=testResults.html"
```