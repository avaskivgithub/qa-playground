using OpenQA.Selenium;

using OpenQA.Selenium.Support.UI;
using Tests.Data;
using Tests.Fixtures;


namespace Tests.TestsUi
{
    //[Parallelizable(ParallelScope.All)]
    [TestFixture("firefox")]
    [TestFixture("chrome")]
    [TestFixture("edge")]
    public class UiTestingPlayground
    {
        private IWebDriver driver;
        private WebDriverWait wait;
        private const int TIMEOUTSecs = 17;
        private readonly string _browser;

        public UiTestingPlayground(string browser)
        {
            _browser = browser;
        }

        [OneTimeSetUp]
        public async Task SetupAsync()
        {
            driver = FixtureWebDriverFactory.CreateDriver(_browser, "--headless");
            driver.Url = MainPage.pageLink;

            wait = new WebDriverWait(driver, TimeSpan.FromSeconds(TIMEOUTSecs));
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
            // Wait for link to be loaded
            IWebElement elemPageHref = wait.Until(drv => drv.FindElement(By.CssSelector(pageHrefLinkLocator)));

            // Click the hyper link
            elemPageHref.Click();

            // Validate
            Assert.That(driver.Url, Is.EqualTo(pageUrl), $"{pageUrl} did not load. Instead it is {driver.Url}");
        }

        [SetUp]
        public void Setup()
        {
            string testName = $"{TestContext.CurrentContext.Test.Name} [{_browser}]";
            TestContext.WriteLine($"Executing: {testName}");

            // Make sure you are on the main page
            driver.Navigate().GoToUrl(MainPage.pageLink);
        }

        // TOBD: tests fail with [Parallelizable(ParallelScope.All)] - why sessions(browser windows) are not closed
/*        
        [SetUp]
        public void Setup()
        {
            driver = FixtureWebDriverFactory.CreateDriver(_browser, "");
            driver.Url = MainPage.pageLink;
            wait = new WebDriverWait(driver, TimeSpan.FromSeconds(TIMEOUTSecs));

            string testName = $"{TestContext.CurrentContext.Test.Name} [{_browser}]";
            TestContext.WriteLine($"Executing: {testName}");
        }

        [TearDown]
        public void Teardown()
        {
            driver.Close();
        }
*/
        [Test]
        //[Ignore("Skipping this test temporarily")]
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

        [Test]
        public async Task NavigateTo_ClientSideDelayPage_CheckTextIsShown()
        {
            // Arrange
            await NavigateFromMainPage_Via_ClickingLink_ValidateOpenedPageUrl(
                MainPage.pageRefClientSideDelay,
                ClientSideDelayPage.pageLink);

            // Act: (click button)
            IWebElement elem = driver.FindElement(By.CssSelector(ClientSideDelayPage.btnAttr));
            elem.Click();

            // Act: (wait for result field to appear)
            // WebDriverWait wait = new WebDriverWait(driver, TimeSpan.FromSeconds(15));
            IWebElement resultActField = wait.Until(drv =>
            {
                var elem = drv.FindElement(By.CssSelector(ClientSideDelayPage.pResultField));
                return elem.Text == ClientSideDelayPage.pResultText ? elem : null;
            });

            // Assert
            Assert.True(ClientSideDelayPage.pResultText == resultActField.Text,
                        $"{ClientSideDelayPage.pResultText} was not shown, instead it was shown {resultActField.Text}");
        }
    }
}