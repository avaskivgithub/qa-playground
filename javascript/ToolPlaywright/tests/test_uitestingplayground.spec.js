// @ts-check
const { test, expect } = require('@playwright/test');
const pages = require('./../../ToolCypress/cypress/e2e/clients/pages');
const utils = require('./clients/utils');

test.beforeEach(async ({ page }) => {
  await page.goto(pages.MainPage.pageLink);
});

test('test Dynamic ID page', async ({ page }) => {
  const testPage = pages.DynamicIdPage;

  await utils.goToPageAndCheckRedirectedLocation(page, pages.MainPage.elementDynamicId, pages.DynamicIdPage.pageLink);

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/Dynamic/);

  await page.getByText(testPage.elementText).click();
  await expect(page.getByText(testPage.elementText)).toBeEnabled();
});

test("test class attr and check that button is enabled", async ({ page }) => {
  const testPage = pages.ClassAttrPage;
  utils.goToPageAndCheckRedirectedLocation(page, pages.MainPage.elementClassAttr, testPage.pageLink);

  await page.locator(testPage.elementAttr).click();
  await expect(page.locator(testPage.elementAttr)).toBeEnabled();  
});

test("test hidden layer, check that green button can not be hit twice", async ({ page }) => {
  const testPage = pages.HiddenLayersPage;

  utils.goToPageAndCheckRedirectedLocation(page, pages.MainPage.elementHiddenLayers, testPage.pageLink);

  await expect(page.locator(testPage.elementHiddenAttr)).toHaveCount(0);

  await page.locator(testPage.elementAttr).click();

  await expect(page.locator(testPage.elementHiddenAttr)).toHaveCount(1);
  await expect(page.locator(testPage.elementAttr)).toBeVisible();
  await expect(page.locator(testPage.elementAttr)).toBeAttached();
  await expect(page.locator(testPage.elementAttr)).not.toBeHidden();
  //await expect(page.locator(testPage.elementAttr)).toHaveCount(0);  ?? TBD: how to check if it is not clickable
});

test("test AJAX request with delay and check result text", async ({ page }) => {
  const testPage = pages.AjaxDelay;
  utils.goToPageAndCheckRedirectedLocation(page, pages.MainPage.elementAjaxDelay, testPage.pageLink);

  await expect(page.locator(testPage.elementResultAttr)).toHaveCount(0);
  await page.locator(testPage.elementAttr).click();
  await page.locator(testPage.elementResultAttr).click({ timeout: 17000 });
  await expect(page.locator(testPage.elementResultAttr)).toHaveCount(1);
});