using OpenQA.Selenium;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium.Edge;
using OpenQA.Selenium.Support.UI;
using System;
using System.Globalization;
using System.Reflection;
using Tests.Data;

public class FixtureWebDriverFactory
{
    private const int TIMEOUTSecs = 30;
    private const int CommandTIMEOUTSecs = 120;

    public static IWebDriver CreateDriver(
        string browserName,
        string optionsArgsStr = "--headless")
    {
        IWebDriver driver;
        TimeSpan commandTimeout = TimeSpan.FromSeconds(CommandTIMEOUTSecs);

        switch (browserName.ToLower())
        {
            case "chrome":
                ChromeOptions optionsChrome = new ChromeOptions();
                ChromeDriverService serviceChrome = ChromeDriverService.CreateDefaultService();

                if (!string.IsNullOrWhiteSpace(optionsArgsStr)) optionsChrome.AddArgument(optionsArgsStr);
                driver = new ChromeDriver(serviceChrome, optionsChrome, commandTimeout);
                break;
            case "firefox":
                FirefoxOptions optionsFirefox = new FirefoxOptions();
                FirefoxDriverService serviceFirefox = FirefoxDriverService.CreateDefaultService();

                if (!string.IsNullOrWhiteSpace(optionsArgsStr)) optionsFirefox.AddArgument(optionsArgsStr);
                driver = new FirefoxDriver(serviceFirefox, optionsFirefox, commandTimeout);
                break;
            case "edge":
                EdgeOptions optionsEdge = new EdgeOptions();
                EdgeDriverService serviceEdge = EdgeDriverService.CreateDefaultService();

                if (!string.IsNullOrWhiteSpace(optionsArgsStr)) optionsEdge.AddArgument(optionsArgsStr);
                driver = new EdgeDriver(serviceEdge, optionsEdge, commandTimeout);
                break;
            default:
                throw new ArgumentException($"Unsupported browser: {browserName}");
        }

        return driver;
    }
    
    // Have to do this to avoid https://stackoverflow.com/questions/66563600/nunit-run-parametrized-tests-in-parallel-with-selenium
    public static (IWebDriver driverInit, WebDriverWait waitInit) SetupDriverAndWaitForParallelRun(string browserInit)
    {
        IWebDriver driverInit = CreateDriver(browserInit, "--headless");
        driverInit.Url = MainPage.pageLink;
        WebDriverWait waitInit = new WebDriverWait(driverInit, TimeSpan.FromSeconds(TIMEOUTSecs));

        return (driverInit, waitInit);
    }

    public static void TeardownDriverForParallelRun(IWebDriver driverInit)
    {
        driverInit.Quit(); // fully terminates the WebDriver session and all background process
                        // opposed to close() that keeps the WebDriver session active
        driverInit.Dispose();
    }

    // Magic of Reflection - TOBD: it doesn't work null is returned by Type.GetType (maybe assembly name is needed)
    public static IWebDriver CreateDriverThroughReflection(string browserName)
    {
        string capitalized = CultureInfo.CurrentCulture.TextInfo.ToTitleCase(browserName.ToLower());
        string optionsClassName = $"OpenQA.Selenium.{capitalized}.{capitalized}Options";
        string driverClassName = $"OpenQA.Selenium.{capitalized}.{capitalized}Driver";

        // Get the Type for Options and Driver
        Type optionsType = Type.GetType(optionsClassName);
        Type driverType = Type.GetType(driverClassName);
        if (optionsType == null || driverType == null)
            throw new ArgumentException($"Unsupported browser: {browserName} AS aftre creation it is {driverType} for {driverClassName}  AND {optionsType} for {optionsClassName}");
        // OPTIONS Setup
        object optionsInstance = Activator.CreateInstance(optionsType);
        optionsInstance.GetType().GetMethod("AddArgument")?.Invoke(optionsInstance, new object[] { "--headless" });

        return (IWebDriver)Activator.CreateInstance(driverType, optionsInstance);
    }
}