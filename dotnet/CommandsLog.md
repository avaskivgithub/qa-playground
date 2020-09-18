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
# unfortunately i had to install ef to make dotnet-aspnet-codegenerator not to fail
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
* Added Details and Add Result to UI
* Adde docker file for RestApi proj, built image and started container
```
qa-playground\dotnet\TestApp> docker build -t avaskiv/restapi .
qa-playground\dotnet\TestApp> docker run -p 5003:5001 avaskiv/restapi

# but there is a network issue
> Get-NetTCPConnection | Where-Object {$_.LocalPort -eq 5003}

LocalAddress                        LocalPort RemoteAddress                       RemotePort State       AppliedSetting OwningProcess
------------                        --------- -------------                       ---------- -----       -------------- -------------
::1                                 5003      ::                                  0          Listen                     16036
::                                  5003      ::                                  0          Listen                     13780

> Invoke-WebRequest 'https://localhost:5003/results'
Invoke-WebRequest : The underlying connection was closed: An unexpected error occurred on a send.
At line:1 char:1
+ Invoke-WebRequest 'https://localhost:5003/results'
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : InvalidOperation: (System.Net.HttpWebRequest:HttpWebRequest) [Invoke-WebRequest], WebException
    + FullyQualifiedErrorId : WebCmdletWebResponseException,Microsoft.PowerShell.Commands.InvokeWebRequestCommand

> (Invoke-WebRequest 'https://localhost:5001/results').Content | convertfrom-json | convertto-json -depth 100
{
    "value":  [
                  {
                      "id":  1,
                      "name":  "11 n",
                      "description":  "desc 6",
                      "res":  1,
                      "error":  "error 6 it was manuall"
                  },
.....
              ],
    "Count":  2
}
```
* [how to ignore ssl certificate errors from Invoke-WebRequest](https://stackoverflow.com/questions/11696944/powershell-v3-invoke-webrequest-https-error)
```
PS C:\Users\andri\AppData\Local\Temp> add-type @"
>>     using System.Net;
>>     using System.Security.Cryptography.X509Certificates;
>>     public class TrustAllCertsPolicy : ICertificatePolicy {
>>         public bool CheckValidationResult(
>>             ServicePoint srvPoint, X509Certificate certificate,
>>             WebRequest request, int certificateProblem) {
>>             return true;
>>         }
>>     }
>> "@
PS C:\Users\andri\AppData\Local\Temp> [System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
PS C:\Users\andri\AppData\Local\Temp> (Invoke-WebRequest 'https://172.23.16.1:5001/results').Content | convertfrom-json | convertto-json -depth 100
{
    "value":  [
                  {
                      "id":  1,
                      "name":  "11 n",
                      "description":  "desc 6",
                      "res":  1,
                      "error":  "error 6 it was manuall"
                  },
                  {
                      "id":  2,
                      "name":  "11 n",
                      "description":  "desc 6",
                      "res":  1,
                      "error":  "error 6 it was manuall"
                  }
              ],
    "Count":  2
}
```
* fixing api staretd within docker
```
qa-playground\dotnet\TestApp\RestApi> Select-String -Pattern 'applicationUrl' -CaseSensitive -SimpleMatch .\Properties\launchSettings.json

Properties\launchSettings.json:7:      "applicationUrl": "http://localhost:37400",
Properties\launchSettings.json:24:      "applicationUrl": "https://0.0.0.0:5001;http://localhost:5000",

# Connected to container
> docker exec -it 1dc579a9e6c2 /bin/bash
root@9bd80d699a48:/app/RestApi# apt-get update; apt-get install -y net-tools; apt-get install -y procps
root@1dc579a9e6c2:/app/RestApi# netstat
Active Internet connections (w/o servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State
tcp        0      0 1dc579a9e6c2:35874      151.101.126.133:80      TIME_WAIT
root@1dc579a9e6c2:/app/RestApi# ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.1  1.0 21207472 68112 ?      SLsl 16:03   0:01 dotnet RestApi.dll
root@1dc579a9e6c2:/app/RestApi# killall dotnet
root@1dc579a9e6c2:/app/RestApi# dotnet RestApi.dll
crit: Microsoft.AspNetCore.Server.Kestrel[0]
      Unable to start Kestrel.
System.IO.IOException: Failed to bind to address http://[::]:80: address already in use.
 ---> Microsoft.AspNetCore.Connections.AddressInUseException: Address already in use
 ---> System.Net.Sockets.SocketException (98): Address already in use
   at System.Net.Sockets.Socket.UpdateStatusAfterSocketErrorAndThrowException(SocketError error, String callerName)
   at System.Net.Sockets.Socket.DoBind(EndPoint endPointSnapshot, SocketAddress socketAddress)
   at System.Net.Sockets.Socket.Bind(EndPoint localEP)
```
* https://medium.com/@the.green.man/set-up-https-on-local-with-net-core-and-docker-7a41f030fc76
```
qa-playground\dotnet\TestApp\RestApi> dotnet user-secrets set "Settings:Secret" "Hidden Secret" --id my-test-secret-from-cli

# %APPDATA%\Microsoft\UserSecret\<secretId>\secrets.json was created

qa-playground\dotnet\TestApp\RestApi> dotnet user-secrets set "Kestrel:Certificates:Development:Password" "Hidden Secret" --id "my-test-secret-from-cli"

dotnet dev-certs https --clean
dotnet dev-certs https `
                 -ep $ENV:UserProfile\.aspnet\https\RestApi.pfx `
                 -p "Hidden Secret"

dotnet dev-certs https --trust

qa-playground\dotnet\TestApp> docker build -t avaskiv/restapi .


docker run --rm -it `
           -p 5000:80 `
           -p 5001:443 `
           -e ASPNETCORE_URLS="https://+;http://+" `
           -e ASPNETCORE_HTTPS_PORT=5001 `
           -e ASPNETCORE_ENVIRONMENT=Development `
           -v $Env:APPDATA\microsoft\UserSecrets\:/root/.microsoft/usersecrets `
           -v $Env:USERPROFILE\.aspnet\https:/root/.aspnet/https/ `
     avaskiv/restapi

crit: Microsoft.AspNetCore.Server.Kestrel[0]
      Unable to start Kestrel.
System.InvalidOperationException: Unable to configure HTTPS endpoint. No server certificate was specified, and the default developer certificate could not be found or is out of date.
To generate a developer certificate run 'dotnet dev-certs https'. To trust the certificate (Windows and macOS only) run 'dotnet dev-certs https --trust'.
For more information on configuring HTTPS see https://go.microsoft.com/fwlink/?linkid=848054.
   at Microsoft.AspNetCore.Hosting.ListenOptionsHttpsExtensions.UseHttps(ListenOptions listenOptions, Action`1 configureOptions)
   at Microsoft.AspNetCore.Hosting.ListenOptionsHttpsExtensions.UseHttps(ListenOptions listenOptions)
   at Microsoft.AspNetCore.Server.Kestrel.Core.Internal.AddressBinder.AddressesStrategy.BindAsync(AddressBindContext context)
   at Microsoft.AspNetCore.Server.Kestrel.Core.Internal.AddressBinder.BindAsync(IServerAddressesFeature addresses, KestrelServerOptions serverOptions, ILogger logger, Func`2 createBinding)
   at Microsoft.AspNetCore.Server.Kestrel.Core.KestrelServer.StartAsync[TContext](IHttpApplication`1 application, CancellationToken cancellationToken)
Unhandled exception. System.InvalidOperationException: Unable to configure HTTPS endpoint. No server certificate was specified, and the default developer certificate could not be found or is out of date.
```
* https://github.com/dotnet/AspNetCore.Docs/issues/6199
```
> cat $Env:APPDATA\Microsoft\UserSecrets\my-test-secret-from-cli\secrets.json
{
  "Settings:Secret": "Hidden Secret",
  "Kestrel:Certificates:Default:Path": "/root/.aspnet/https/RestApi.pfx",
  "Kestrel:Certificates:Default:Password": "Hidden Secret"
}
```
* Generate ssl certificates using [following instructions](https://geekflare.com/openssl-commands-certificates/)
```
# private key used on the server
> openssl req -out geekflare.csr -newkey rsa:2048 -nodes -keyout geekflare.key
# public key
> openssl req -x509 -sha256 -nodes -days 7300 -newkey rsa:2048 -keyout gfselfsigned.key -out gfcert.pem
```
* ssl certificate is killing, try https://docs.microsoft.com/en-us/aspnet/core/security/docker-https?view=aspnetcore-3.1#windows-using-linux-containers
```
dotnet dev-certs https -ep $env:USERPROFILE\.aspnet\https\aspnetapp.pfx -p "Hidden Secret"
dotnet dev-certs https --trust
# docker pull mcr.microsoft.com/dotnet/core/samples:aspnetapp
qa-playground\dotnet\TestApp> docker build -t avaskiv/restapi .
docker run --rm -it `
		-p 5000:80 `
		-p 5001:5001 `
		-e ASPNETCORE_URLS="https://+;http://+" `
		-e ASPNETCORE_HTTPS_PORT=5001 `
		-e ASPNETCORE_Kestrel__Certificates__Default__Password="Hidden Secret" `
		-e ASPNETCORE_Kestrel__Certificates__Default__Path=/app/RestApi/aspnetapp.pfx `
        avaskiv/restapi
#		-v $env:USERPROFILE\.aspnet\https:/https/ `
#        mcr.microsoft.com/dotnet/core/samples:aspnetapp

> docker ps
CONTAINER ID        IMAGE               COMMAND
89df291d8451        avaskiv/restapi     "dotnet RestApi.dll"   
PS C:\Users\andri> docker exec -it 89df291d8451 /bin/bash
root@89df291d8451:/app/RestApi# curl -k 'https://localhost:5001/results'
[]root@89df291d8451:/app/RestApi#
```

## TBD
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