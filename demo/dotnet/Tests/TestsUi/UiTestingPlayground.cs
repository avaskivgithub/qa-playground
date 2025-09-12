using OpenQA.Selenium;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Chrome;
using Tests.Data;
using Tests.Fixtures;

namespace Tests.TestsUi
{
    [TestFixture("firefox")]
    [TestFixture("chrome")]
    public class UiTestingPlayground
    {
        private IWebDriver driver;
        private readonly string _browser;

        public UiTestingPlayground(string browser)
        {
            _browser = browser;
        }

        [OneTimeSetUp]
        public async Task SetupAsync()
        {
            driver = FixtureWebDriverFactory.CreateDriver(_browser);
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

        [SetUp]
        public void Setup()
        {
            string testName = $"{TestContext.CurrentContext.Test.Name} [{_browser}]";
            TestContext.WriteLine($"Executing: {testName}");
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