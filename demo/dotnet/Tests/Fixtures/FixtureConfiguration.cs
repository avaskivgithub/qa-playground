// using System.Reflection;
using Microsoft.Extensions.Configuration;
// using Microsoft.Extensions.Configuration.Json;


namespace Tests.Fixtures
{
    public static class FixtureConfiguration
    {
        static private readonly IConfiguration Configuration = new ConfigurationBuilder()
                //.SetBasePath(Path.GetDirectoryName(Assembly.GetEntryAssembly().Location))
                //.SetBasePath(System.IO.Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.test.json", optional: false, reloadOnChange: true)
                .Build();
        /*
        var builder = new ConfigurationBuilder()
            .SetBasePath(Directory.GetCurrentDirectory())
            .AddJsonFile("appsettings.json", optional: true, reloadOnChange: true)
            .AddJsonFile($"appsettings.{Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT")}.json", optional: true, reloadOnChange: true)
            .AddEnvironmentVariables();
        */

        public static string GetSetting(string settingName)
        {
            return Configuration[settingName];
        }
    }
}