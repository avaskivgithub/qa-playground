using OpenQA.Selenium;
using OpenQA.Selenium.Firefox;
using Tests.Data;

namespace Tests.TestsUi
{
    [TestFixture]
    public class UiTestingPlayground
    {
        private IWebDriver driver;

        [OneTimeSetUp]
        public async Task SetupAsync()
        {

            FirefoxOptions options = new FirefoxOptions();
            options.AddArgument("--headless");

            driver = new FirefoxDriver(options);
            driver.Url = MainPage.pageLink;
            // System.Threading.Thread.Sleep(2000);
        }


        [OneTimeTearDown]
        public async Task TeardownAsync()
        {
            // System.Threading.Thread.Sleep(2000);
            driver.Close();
        }

        [Test]
        public async Task DynamicPage()
        {
            string testPage = DynamicIdPage.pageLink;
            IWebElement elemPageHref = driver.FindElement(By.CssSelector(MainPage.pageRefDynamicId));
            elemPageHref.Click();

            string currentUrl = driver.Url;
            // driver.Navigate().GoToUrl(testPage);

            Assert.That(driver.Url, Is.EqualTo(testPage), $"{testPage} did not load. Instead it is {driver.Url}");
            IWebElement elem = driver.FindElement(By.CssSelector(DynamicIdPage.btnAttr));
            Assert.True(elem.Enabled, "Button was not enabled");

        }
    }
}