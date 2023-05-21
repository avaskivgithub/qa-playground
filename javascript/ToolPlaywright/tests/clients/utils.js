const { expect } = require('@playwright/test');

async function goToPageAndCheckRedirectedLocation(page, elementHref, pageLink, timeoutValue=2000){
  await page.locator(elementHref, { timeout: timeoutValue }).click();
  await expect(page.url()).toBe(pageLink);

}

exports.goToPageAndCheckRedirectedLocation = goToPageAndCheckRedirectedLocation;