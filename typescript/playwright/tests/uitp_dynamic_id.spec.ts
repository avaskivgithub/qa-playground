import { test, expect } from '@playwright/test';


test('test dynamic id', async ({ page }) => {
  // Go to http://www.uitestingplayground.com/dynamicid
  await page.goto('/dynamicid');
  // Click text=Button with Dynamic ID
  await page.click('text=Button with Dynamic ID');
  // Click text=Button with Dynamic ID
  await page.click('text=Button with Dynamic ID');


  let locator = page.locator('text=Button with Dynamic ID');
  let re = /\w+/
  await expect(locator).toHaveAttribute('id', re);
  await expect(locator).toHaveAttribute('type', 'button');
});