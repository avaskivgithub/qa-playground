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
* To match python version added SystemTestsRestApi.Clients, which are test services (helpers) to setup / call db and rest api
```
# for HttpTestClient https://stackoverflow.com/questions/19158378/httpclient-not-supporting-postasjsonasync-method-c-sharp
dotnet add package Microsoft.AspNet.WebApi.Client --version 5.2.7
```
* Moved Data into a separate project and the same for Models
```
qa-playground\dotnet\TestApp> dotnet new classlib -n DataRepository -o DataRepository
qa-playground\dotnet\TestApp> dotnet add .\RestApi\RestApi.csproj reference .\DataRepository\DataRepository.csproj
# for the access to Models
qa-playground\dotnet\TestApp> dotnet add .\RestApi\RestApi.csproj reference .\Models\Models.csproj
qa-playground\dotnet\TestApp> dotnet add .\DataRepository\DataRepository.csproj reference .\Models\Models.csproj
```
* Used Data in test project and filled in setup step of the recreatig empty db in the init test
```
qa-playground\dotnet\TestApp> dotnet add .\SystemTestsRestApi\SystemTestsRestApi.csproj reference .\DataRepository\DataRepository.csproj
```
* Added system tests using xunit for /results and /results/{resultId} endpoints
```
qa-playground\dotnet\TestApp\SystemTestsRestApi> dotnet test
qa-playground\dotnet\TestApp\SystemTestsRestApi> dotnet test
Test run for C:\Users\andri\Documents\Projects\2020\qa-playground\dotnet\TestApp\SystemTestsRestApi\bin\Debug\netcoreapp3.1\SystemTestsRestApi.dll(.NETCoreApp,Version=v3.1)
Microsoft (R) Test Execution Command Line Tool Version 16.6.0
Copyright (c) Microsoft Corporation.  All rights reserved.

Starting test execution, please wait...

A total of 1 test files matched the specified pattern.

Test Run Successful.
Total tests: 2
     Passed: 2
 Total time: 1.7103 Seconds
```
* Add UI mvc. A bit confusing, so have to go through [training](https://docs.microsoft.com/en-us/aspnet/core/tutorials/first-mvc-app/start-mvc?view=aspnetcore-3.1&tabs=visual-studio-code) cearfly
```
qa-playground\dotnet\TestApp> dotnet new mvc -n UImvc -o UImvc
qa-playground\dotnet> dotnet sln TestApp add .\TestApp\UImvc\UImvc.csproj

# changed port from 5000s to 6000s
qa-playground\dotnet> Select-String -Pattern 'applicationUrl' -CaseSensitive -SimpleMatch .\TestApp\UImvc\Properties\launchSettings.json
TestApp\UImvc\Properties\launchSettings.json:6:      "applicationUrl": "http://localhost:47628",
TestApp\UImvc\Properties\launchSettings.json:21:      "applicationUrl": "https://localhost:6001;http://localhost:6000",
```
* Added to the vc template project Results controller / view / model, but need to figure out foreach in the results view razor page
```
# added Results to the navbar-nav in the UImvc/Views/Shared/_Layout.cshtml to have Results tab
```
* Trying scaffolding
```
dotnet tool install --global dotnet-aspnet-codegenerator
dotnet add package Microsoft.VisualStudio.Web.CodeGeneration.Design
# unfortunatelly i had to install ef to make dotnet-aspnet-codegenerator not to fail
dotnet add package Microsoft.EntityFrameworkCore.Design
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.SQLite

# Added Data\MvcResultContext.cs

# Startup.cs
using UImvc.Data;
using Microsoft.EntityFrameworkCore;
...
public void ConfigureServices(IServiceCollection services)
{
    services.AddControllersWithViews();
    
    services.AddDbContext<MvcMovieContext>(options =>
            options.UseSqlite(Configuration.GetConnectionString("MvcMovieContext")));
}

# appsettings*.json
  "ConnectionStrings": {
    "MvcResultContext": "Data Source=MvcResult.db"
  }


dotnet aspnet-codegenerator controller -name ResultController -m Result -dc MvcResultContext --relativeFolderPath Controllers --useDefaultLayout --referenceScriptLibraries

# create db
dotnet tool install --global dotnet-ef
dotnet ef migrations add InitialCreate
dotnet ef database update

# start app
dotnet run

# go to https://localhost:6001/Result
```
* NEXT: remove ef and figure out why results model was not working. Instead of db use rest api
```
# @foreach referes to the set of data as Model and model itself is defined by 
# @model IEnumerable<UImvc.Models.ResultsViewModel>
```

## TBD
* Add UI using /results and /results/{resultId} endpoints (for now only table with results and view details for 1 result)
* Add authentication to the api
* Add docstrings using [Microsoft documentation](https://docs.microsoft.com/en-us/dotnet/csharp/language-reference/language-specification/documentation-comments)
* Add logging
```
// nugets to check
Microsoft.Extensions.Hosting
Serilog.Extensions.Hosting
Serilog.Settings.Configuration
Serilog.Sinks.Console
```