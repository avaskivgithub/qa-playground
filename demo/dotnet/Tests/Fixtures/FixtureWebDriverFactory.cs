using OpenQA.Selenium;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Chrome;
using System;
using System.Globalization;
using System.Reflection;

public class FixtureWebDriverFactory
{

    public static IWebDriver CreateDriver(string browserName)
    {
        IWebDriver driver;
        switch (browserName.ToLower())
        {
            case "chrome":
                ChromeOptions optionsChrome = new ChromeOptions();
                optionsChrome.AddArgument("--headless");
                driver = new ChromeDriver(optionsChrome);
                break;
            case "firefox":
                FirefoxOptions optionsFirefox = new FirefoxOptions();
                optionsFirefox.AddArgument("--headless");
                driver = new FirefoxDriver(optionsFirefox);
                break;
            default:
                throw new ArgumentException($"Unsupported browser: {browserName}");
        }

        return driver;
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