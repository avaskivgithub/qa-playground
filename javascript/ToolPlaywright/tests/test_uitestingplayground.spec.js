// @ts-check
const { test, expect } = require('@playwright/test');
const pages = require('./../../ToolCypress/cypress/e2e/clients/pages');
const utils = require('./clients/utils');

test.beforeEach(async ({ page }) => {
  await page.goto(pages.MainPage.pageLink);
});

test('test Dynamic ID page', async ({ page }) => {
  const testPage = pages.DynamicIdPage;

  await utils.goToPageAndCheckRedirectedLocation(page, pages.MainPage.pageRefDynamicId, pages.DynamicIdPage.pageLink);

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/Dynamic/);

  await page.getByText(testPage.btnText).click();
  await expect(page.getByText(testPage.btnText)).toBeEnabled();
});

test("test class attr and check that button is enabled", async ({ page }) => {
  const testPage = pages.ClassAttrPage;
  utils.goToPageAndCheckRedirectedLocation(page, pages.MainPage.pageRefClassAttr, testPage.pageLink);

  await page.locator(testPage.btnAttr).click();
  await expect(page.locator(testPage.btnAttr)).toBeEnabled();  
});

test("test hidden layer, check that green button can not be hit twice", async ({ page }) => {
  const testPage = pages.HiddenLayersPage;

  utils.goToPageAndCheckRedirectedLocation(page, pages.MainPage.pageRefHiddenLayers, testPage.pageLink);

  await expect(page.locator(testPage.btnHiddenAttr)).toHaveCount(0);

  await page.locator(testPage.btnAttr).click();

  await expect(page.locator(testPage.btnHiddenAttr)).toHaveCount(1);
  await expect(page.locator(testPage.btnAttr)).toBeVisible();
  await expect(page.locator(testPage.btnAttr)).toBeAttached();
  await expect(page.locator(testPage.btnAttr)).not.toBeHidden();
  //await expect(page.locator(testPage.elementAttr)).toHaveCount(0);  ?? TBD: how to check if it is not clickable
});

test("test AJAX request with delay and check result text", async ({ page }) => {
  const testPage = pages.AjaxDelay;
  utils.goToPageAndCheckRedirectedLocation(page, pages.MainPage.pageRefAjaxDelay, testPage.pageLink);

  await expect(page.locator(testPage.btnResultAttr)).toHaveCount(0);
  await page.locator(testPage.btnAttr).click();
  await page.locator(testPage.btnResultAttr).click({ timeout: 17000 });
  await expect(page.locator(testPage.btnResultAttr)).toHaveCount(1);
});