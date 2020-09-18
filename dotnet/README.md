# dotnet
A playground for testing a "Test App" written using DotNet.

## TestApp
"Test App":
* Uses sqlite as a backend with a single table Results that has (Id, Name, Description, Res, Error) fields
* REST Api ( https://localhost:5001/results ) to do CRUD operations on the Results table records
* MVC UI https://localhost:6001/ that talks to REST Api 

### Setup
Start both REST Api and MVC UI (each in separate terminal)
```
# open terminal and cd qa-playground\dotnet\TestApp\RestApi
qa-playground\dotnet\TestApp\RestApi> dotnet restore
qa-playground\dotnet\TestApp\RestApi> dotnet build
qa-playground\dotnet\TestApp\RestApi> dotnet run
# open one more terminal and cd qa-playground\dotnet\TestApp\UImvc
qa-playground\dotnet\TestApp\UImvc> dotnet restore
qa-playground\dotnet\TestApp\UImvc> dotnet build
qa-playground\dotnet\TestApp\UImvc> dotnet run
```

### Run Application
* Open UI https://localhost:6001, go to Results and add couple of records
* Get list of results from REST Api
```
> (Invoke-WebRequest 'https://localhost:5001/results').Content | convertfrom-json | convertto-json -depth 100
```

### System Tests
To run system tests for the REST API make sure that it's started locally 
```
qa-playground\dotnet\TestApp\RestApi> dotnet run
```
Now run the system tests
```
qa-playground\dotnet\TestApp> dotnet test
Starting test execution, please wait...

A total of 1 test files matched the specified pattern.

Test Run Successful.
Total tests: 2
     Passed: 2
 Total time: 5.9381 Seconds
```

### Docker
To start REST Api in docker container:
* Install docker (for windows https://www.docker.com/products/docker-desktop )
* Build image
```
qa-playground\dotnet\TestApp> docker build -t testdocker/restapi .
```
* Start api in a docker container
```
docker run --rm -it `
        -p 5001:5001 `
        -e ASPNETCORE_Kestrel__Certificates__Default__Password="Hidden Secret" `
        -e ASPNETCORE_Kestrel__Certificates__Default__Path=/app/RestApi/aspnetapp.pfx `
        testdocker/restapi
```

## Learning materials
* [Tim Corey's video: Introduction to ASP.NET MVC in C#: Basics, Advanced Topics, Tips, Tricks, Best Practices, and More](https://youtu.be/phyV-OQNeRM)
* [Les Jackson's video: .NET Core 3.1 MVC REST API - Full Course](https://www.youtube.com/watch?v=fmvcAzHpsk8&feature=youtu.be)
* [Tim Corey's video: Introduction to ASP.NET Core MVC in C# plus LOTS of Tips](https://www.youtube.com/watch?v=1ck9LIBxO14)
* [Microsoft Documentation: Recomended Learning Path for ASP.NET](https://docs.microsoft.com/en-us/aspnet/core/introduction-to-aspnet-core?view=aspnetcore-3.1#recommended-learning-path)
* [Github: Sample apps for Microsoft Learn modules using ASP.NET Core](https://github.com/MicrosoftDocs/mslearn-aspnet-core/tree/master/modules/create-razor-pages-aspnet-core/src)

## Commands
See [CommandsLog.md](CommandsLog.md) for step by step commands, but keep in mind that it's a log and as a result with not condensed information.