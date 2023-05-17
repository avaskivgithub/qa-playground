const pages = require('../../../pages_uitestingplayground');
const utils = require('../clients/utils');
const {By, Builder, Browser} = require('selenium-webdriver');
const {suite} = require('selenium-webdriver/testing');
const assert = require("assert");
require("chromedriver");

suite(function (env) {
  describe('Uitestingplayground set', function () {
    let driver;

    before(async function () {
      driver = await new Builder()
        .forBrowser('chrome')
        //.usingServer('http://localhost:4444/wd/hub')
        .build();
    });

    beforeEach(async function () {
      await driver.get(pages.MainPage.pageLink);
    });

    after(async () => await driver.quit());

    it('Dynamic Id', async function () {
      const testPage = pages.DynamicIdPage;
     await utils.goToPageAndCheckRedirectedLocation(driver, pages.MainPage.pageRefDynamicId, testPage.pageLink);

      let testButton = await driver.findElement(By.css(testPage.btnAttr));
      await testButton.click();

      let value = await testButton.getText();
      assert.equal(testPage.btnText, value);
    });
  });
}, { browsers: [Browser.CHROME, Browser.FIREFOX]});