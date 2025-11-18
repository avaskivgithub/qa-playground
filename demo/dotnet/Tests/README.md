# Overview

## AUT - API
API being used as an example for testing is:
- https://reqres.in/signup - Free API Key
- https://reqres.in/api-docs/

## Selenium UI
### Webdrivers
For Selenium webdrivers is used WebDriverManager (installed via `dotnet add package WebDriverManager`)
- https://github.com/rosolko/WebDriverManager.Net/blob/master/README.md#usage
```
new DriverManager().SetUpDriver(<config>) does magic for you:
1. It checks the latest version of the WebDriver binary file
2. It downloads the binary WebDriver if it is not present in your system
So far, WebDriverManager supports Chrome, Microsoft Edge, Firefox(Marionette), Internet Explorer, Opera or PhantomJS configs
```
To list existing webdrivers on Windows run from the user home directory:
```
ls .\.wdm\drivers\
```
But by using `new DriverManager().SetUpDriver(<config>)` they will be downloaded to the bin\Debug\net<version> directory


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
- To run tests all or from the specific folder
```
cd .\qa-playground\demo\dotnet\Tests
dotnet clean; dotnet test --settings test.runsettings --logger "console;verbosity=detailed"
dotnet clean; dotnet test --settings test.runsettings --logger "console;verbosity=detailed" --filter FullyQualifiedName~Tests.TestsApi
```
- To run tests with html results
```
dotnet clean; dotnet test --settings test.runsettings --logger "html;logfilename=testResults.html"
```