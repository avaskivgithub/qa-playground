using Microsoft.Extensions.Configuration;


namespace Tests.Fixtures
{
    public static class FixtureConfiguration
    {
        static private readonly IConfiguration Configuration = new ConfigurationBuilder()
                .AddJsonFile("appsettings.test.json", optional: false, reloadOnChange: true)
                .Build();

        public static string GetSetting(string settingName)
        {
            return Configuration[settingName];
        }
    }
}