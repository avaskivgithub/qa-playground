const {By} = require('selenium-webdriver');
const assert = require("assert");

async function goToPageAndCheckRedirectedLocation(driver, elementHref, pageLink, timeoutValue=2000){
  let ref = driver.findElement(By.css(elementHref));
  await ref.click();

  await driver.manage().setTimeouts({implicit: timeoutValue});

  let actualPageLink = await driver.getCurrentUrl();
  assert.equal(pageLink, actualPageLink);
}

exports.goToPageAndCheckRedirectedLocation = goToPageAndCheckRedirectedLocation;