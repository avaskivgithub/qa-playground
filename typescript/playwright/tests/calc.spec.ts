import { test, expect } from '@playwright/test';
import { CalcDemo } from "../pages/calc_demo";

let calcPage = new CalcDemo();


test('calc add 2 numbers', async ({page}) => {

    // Go to https://specflowoss.github.io/Calculator-Demo/Calculator.html
    await page.goto('https://specflowoss.github.io/Calculator-Demo/Calculator.html');
    
    await calcPage.enter_num_1(page, 1);
    //await page.press(calcPage.get_selector_btn_1(), 'Tab');
    await calcPage.enter_num_2(page, 2);
    await calcPage.add_numbers(page);

    await expect(calcPage.get_result_locator(page)).toHaveValue('3');
});