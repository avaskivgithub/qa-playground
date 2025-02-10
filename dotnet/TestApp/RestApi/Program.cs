using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using System.Net;

namespace RestApi
{
    public class Program
    {
        public static void Main(string[] args)
        {
            CreateHostBuilder(args).Build().Run();
        }

        public static IHostBuilder CreateHostBuilder(string[] args) =>
            Host.CreateDefaultBuilder(args)
            // https://github.com/dotnet/AspNetCore.Docs/blob/master/aspnetcore/fundamentals/servers/kestrel/samples/3.x/KestrelSample/Program.cs
            // https://docs.microsoft.com/en-us/aspnet/core/fundamentals/servers/kestrel?view=aspnetcore-3.1
            // ssl certificate generated using: https://docs.microsoft.com/en-us/aspnet/core/security/docker-https?view=aspnetcore-3.1#windows-using-linux-containers
            //                 
                .ConfigureWebHostDefaults(webBuilder =>
                {
                    webBuilder.ConfigureKestrel(serverOptions =>
                    {
                        /*
                            // https://medium.com/@the.green.man/set-up-https-on-local-with-net-core-and-docker-7a41f030fc76
                            dotnet user-secrets set "Kestrel:Certificates:Development:Password" "Hidden Secret"

                            TestApp\RestApi> dotnet dev-certs https --clean
                            TestApp\RestApi> dotnet dev-certs https -ep aspnetapp.pfx -p "Hidden Secret"
                            TestApp\RestApi> dotnet dev-certs https --trust
                            TestApp\RestApi> dotnet user-secrets -p .\RestApi.csproj init
                            TestApp\RestApi> dotnet user-secrets -p .\RestApi.csproj set "Kestrel:Certificates:Development:Password" "Hidden Secret"

                            To get rid of net::ERR_CERT_INVALID go to:
                            chrome://flags/#allow-insecure-localhost and disable 'WebTransport Developer Mode'

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
                        */
                        // right way to do
                        var configuration = (IConfiguration)serverOptions.ApplicationServices.GetService(typeof(IConfiguration));
                        var certPassword = configuration.GetValue<string>("Kestrel:Certificates:Default:Password");
                        var certPath = configuration.GetValue<string>("Kestrel:Certificates:Default:Path");
                        // to avoid a lot of readme instructions hardcoded values here
                        certPassword = "Hidden Secret";
                        certPath = "aspnetapp.pfx";

                        serverOptions.Listen(IPAddress.Any, 5000);
                        serverOptions.Listen(IPAddress.Any, 5001, 
                            listenOptions =>
                            {
                                listenOptions.UseHttps(certPath, certPassword);
                            });
                    })
                    .UseStartup<Startup>();
                });
    }
}
