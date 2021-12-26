//import { test } from '@playwright/test';

export class CalcDemo {
    field_1: string;
    field_2: string;
    button_add: string;
    result: string;
   
    constructor() {
      this.field_1 = '[placeholder="First number"]';
      this.field_2 = '[placeholder="Second number"]';
      this.button_add = 'text=Add';
      this.result = 'input[name="result"]'
    }
   
    get_selector_field_1() {
      return this.field_1
    }

    get_selector_field_2() {
        return this.field_2
      }

    async enter_num_1(page, num: number){
        await page.click(this.field_1);
        await page.fill(this.field_1, num.toString());    
    }

    async enter_num_2(page, num: number){
        await page.click(this.field_2);
        await page.fill(this.field_2, num.toString());     
    }

    async add_numbers(page){
        await page.click(this.button_add);
    }

    get_result_locator(page){
        return page.locator(this.result)
    }
  }