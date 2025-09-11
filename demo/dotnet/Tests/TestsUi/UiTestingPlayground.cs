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
        }


        [OneTimeTearDown]
        public async Task TeardownAsync()
        {
            // System.Threading.Thread.Sleep(2000);
            driver.Close();
        }

        public async Task NavigateFromMainPage_Via_ClickingLink_ValidateOpenedPageUrl(
            string pageHrefLinkLocator,
            string pageUrl)
        { 
            // driver.Navigate().GoToUrl(pageUrl);

            // Click the hyper link
            IWebElement elemPageHref = driver.FindElement(By.CssSelector(pageHrefLinkLocator));
            elemPageHref.Click();

            // Validate
            Assert.That(driver.Url, Is.EqualTo(pageUrl), $"{pageUrl} did not load. Instead it is {driver.Url}");
        }

        [Test]
        public async Task NavigateTo_DynamicPage_CheckBtnEnabled()
        {
            // Arrange
            await NavigateFromMainPage_Via_ClickingLink_ValidateOpenedPageUrl(
                MainPage.pageRefDynamicId,
                DynamicIdPage.pageLink);

            // Act (find the element)
            IWebElement elem = driver.FindElement(By.CssSelector(DynamicIdPage.btnAttr));

            // Assert
            Assert.True(elem.Enabled, "Button was not enabled");
        }
    }
}