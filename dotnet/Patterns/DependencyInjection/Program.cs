using System;
using System.IO;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Serilog;

namespace DependencyInjection
{
    class Program
    {
        static void Main(string[] args)
        {
            // Setting up Serilog section
            var builder = new ConfigurationBuilder();
            BuildConfig(builder);

            Serilog.Log.Logger = new LoggerConfiguration()
                .ReadFrom.Configuration(builder.Build())
                .Enrich.FromLogContext()
                .WriteTo.Console()
                .CreateLogger();

            Serilog.Log.Information("Application Starting");

            // Setting up Dependency Injection
            var host = Host.CreateDefaultBuilder()
                .ConfigureServices((context, services) => 
                {
                    services.AddTransient<IGreetingService, GreetingService>();

                })
                .UseSerilog()
                .Build();

            var srvc = ActivatorUtilities.CreateInstance<GreetingService>(host.Services);
            srvc.Run();
        }

        // Do loging before we load configuration
        static void BuildConfig(IConfigurationBuilder builder)
        {
            // Setting up Serilog Configuration section
            builder.SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
                .AddJsonFile($"appsettings.{Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT") ?? "Production"}.json", optional: true)
                .AddEnvironmentVariables();;
        }
    }
}
