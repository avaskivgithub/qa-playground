using OpenQA.Selenium;

using OpenQA.Selenium.Support.UI;
using Tests.Data;
using Tests.Fixtures;


// https://stackoverflow.com/questions/66563600/nunit-run-parametrized-tests-in-parallel-with-selenium 
// - creating the driver twice through [SetUp], but both instances are stored in the same member field, driver
//   which causes sharing state between tests
// - the ParallelizableAttribute is used to tell NUnit that the test may be run in parallel. 
//   NUnit accepts that as a promise, but if you share state between tests they won't run correctly
namespace Tests.TestsUi
{
    [Parallelizable(ParallelScope.All)]
    [TestFixture("firefox")]
    [TestFixture("chrome")]
    [TestFixture("edge")]
    public class UiTestingPlayground
    {
        private readonly string _browser;

        public UiTestingPlayground(string browser)
        {
            _browser = browser;
        }

        [SetUp]
        public void Setup()
        {
            string testName = $"{TestContext.CurrentContext.Test.Name} [{_browser}]";
            TestContext.WriteLine($"Executing: {testName}");
        }

        public async Task NavigateFromMainPage_Via_ClickingLink_ValidateOpenedPageUrl(
            string pageHrefLinkLocator,
            string pageUrl,
            IWebDriver driverInit,
            WebDriverWait waitInit)
        {
            // Wait for link to be loaded
            IWebElement elemPageHref = waitInit.Until(drv => drv.FindElement(By.CssSelector(pageHrefLinkLocator)));

            // Click the hyper link
            elemPageHref.Click();

            // Validate
            Assert.That(driverInit.Url, Is.EqualTo(pageUrl), $"{pageUrl} did not load. Instead it is {driverInit.Url}");
        }

        [Test]
        //[Ignore("Skipping this test temporarily")]
        public async Task NavigateTo_DynamicPage_CheckBtnEnabled()
        {
            IWebDriver driverTest;
            WebDriverWait waitTest;
            (driverTest, waitTest) = FixtureWebDriverFactory.SetupDriverAndWaitForParallelRun(_browser);
            try
            {
                // Arrange
                await NavigateFromMainPage_Via_ClickingLink_ValidateOpenedPageUrl(
                    MainPage.pageRefDynamicId,
                    DynamicIdPage.pageLink,
                    driverTest,
                    waitTest);

                // Act (find the element)
                IWebElement elem = driverTest.FindElement(By.CssSelector(DynamicIdPage.btnAttr));

                // Assert
                Assert.True(elem.Enabled, "Button was not enabled");
            }
            finally
            {
                FixtureWebDriverFactory.TeardownDriverForParallelRun(driverTest);
            }
        }

        [Test]
        public async Task NavigateTo_ClientSideDelayPage_CheckTextIsShown()
        {
            IWebDriver driverTest;
            WebDriverWait waitTest;
            (driverTest, waitTest) = FixtureWebDriverFactory.SetupDriverAndWaitForParallelRun(_browser);
            try
            {
                // Arrange
                await NavigateFromMainPage_Via_ClickingLink_ValidateOpenedPageUrl(
                    MainPage.pageRefClientSideDelay,
                    ClientSideDelayPage.pageLink,
                    driverTest,
                    waitTest);

                // Act: (click button)
                IWebElement elem = driverTest.FindElement(By.CssSelector(ClientSideDelayPage.btnAttr));
                elem.Click();

                // Act: (wait for result field to appear)
                IWebElement resultActField = waitTest.Until(drv =>
                {
                    var elem = drv.FindElement(By.CssSelector(ClientSideDelayPage.pResultField));
                    return elem.Text == ClientSideDelayPage.pResultText ? elem : null;
                });

                // Assert
                Assert.True(ClientSideDelayPage.pResultText == resultActField.Text,
                            $"{ClientSideDelayPage.pResultText} was not shown, instead it was shown {resultActField.Text}");
            }
            finally
            {
                FixtureWebDriverFactory.TeardownDriverForParallelRun(driverTest);
            }
        }
    }
}