## Commands
Track commands and larning path:
* Create Rest Api project with TestApp solution
```
# from the root repo directory
qa-playground> cd dotnet

qa-playground\dotnet> dotnet new webapi -n RestApi -o TestApp
qa-playground\dotnet\TestApp> dotnet restore
qa-playground\dotnet\TestApp> dotnet build
qa-playground\dotnet\TestApp> dotnet run
# by default: https://localhost:5001/weatherforecast
# remove deafault weatherforecast

# add Models.Results and ResultsController
qa-playground\dotnet\TestApp> dotnet run
# get: https://localhost:5001/results

# create solution and add RestApi
qa-playground\dotnet\TestApp> dotnet new sln
qa-playground\dotnet\TestApp> cd ..
qa-playground\dotnet> dotnet sln TestApp add TestApp/RestApi.csproj
Project `RestApi.csproj` added to the solution.
qa-playground\dotnet> dotnet sln TestApp list
Project(s)
----------
RestApi.csproj
PS C:\Users\andri\Documents\Projects\2020\qa-playground\dotnet> 
```
* Sqlite with dapper based on [Sergey Maskalik's blog](https://blog.maskalik.com/asp-net/sqlite-simple-database-with-dapper/)
```
qa-playground\dotnet\TestApp> dotnet add package System.Data.SQLite.Core --version 1.0.113.1
qa-playground\dotnet\TestApp> dotnet add package Dapper

# base on the blog example created RestApi.Data
```
* Still can build and run
```
qa-playground\dotnet\TestApp> dotnet build .\RestApi.csproj
qa-playground\dotnet\TestApp> dotnet run

# get: https://localhost:5001/results
```
* Reorganized by moving RestApi project into it's own subfolder
```
qa-playground\dotnet> dotnet sln TestApp remove TestApp/RestApi.csproj

# from Git Bash
andri@LAPTOP-2K696J8H MINGW64 ~/Documents/Projects/2020/qa-playground/dotnet/TestApp
$ for file in $(ls | grep -v 'RestApi' | grep -v 'TestApp.sln'); do git mv $file RestApi; done;

# back from Visual Studio Code
qa-playground\dotnet\TestApp> rm -r bin
qa-playground\dotnet\TestApp> rm -r obj
qa-playground\dotnet\TestApp> git mv .\RestApi.csproj .\RestApi\
qa-playground\dotnet\TestApp> dotnet sln add .\RestApi\RestApi.csproj

# check that we are ok
qa-playground\dotnet\TestApp> dotnet build .\RestApi\RestApi.csproj
qa-playground\dotnet\TestApp> cd .\RestApi\
qa-playground\dotnet\TestApp\RestApi> dotnet run

# get: https://localhost:5001/results
```
* Updated ResultsController with 3 endpoints ( /results, /results/{id}, /create/db/seeddata) which uses RestApi.Data.IResultsRepository.After calling https://localhost:5001/create/db/seeddata  data were seeded into the db:
```
qa-playground\dotnet\TestApp\RestApi> sqlite3 .\sqlitetest.db
SQLite version 3.32.3 2020-06-18 14:00:33
Enter ".help" for usage hints.
sqlite> select * from Results;
1|Name1|Description1|0|Error1
2|Name2|Description2|1|Error2
3|Name3|Description3|1|Error3
sqlite> .exit
```
* xunit tests for RestApi. [Getting started doc](https://xunit.net/docs/getting-started/netcore/cmdline)
```
qa-playground\dotnet\TestApp> dotnet new xunit -n SystemTestsRestApi -o SystemTestsRestApi
qa-playground\dotnet\TestApp> cd ..
qa-playground\dotnet> dotnet sln TestApp add .\TestApp\SystemTestsRestApi\SystemTestsRestApi.csproj
qa-playground\dotnet> cd .\TestApp\SystemTestsRestApi\
qa-playground\dotnet\TestApp\SystemTestsRestApi> dotnet test

```

## TBD
* Add system tests using xunit for /results and /results/{resultId} endpoints
* Add authentication to the api
* Add docstrings using [Microsoft documentation](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/language-specification/documentation-comments)