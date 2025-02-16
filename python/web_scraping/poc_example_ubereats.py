"""
README: 
        1. collect data from UberEats restaurant pages (for now just 1 page)
        2. get Menu Items: Names, Prices
        3. the result saved into menu.csv
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

def scroll_and_get_all_data(driver, selector, selector_type=By.CSS_SELECTOR):
    all_data = []

    # Initialize data in pixels for scrolling
    step_height = driver.execute_script("return window.innerHeight;")
    last_height = driver.execute_script("return window.scrollY;")

    # Start collecting data from the page
    while True:
        try:
            elems = driver.find_elements(selector_type, selector)
            list = [el.text for el in elems]
            all_data.extend(list)

            # Scroll down by view port height
            driver.execute_script("window.scrollBy({ top: %s });" % step_height)
            time.sleep(5) 
            # driver.implicitly_wait(2)
        except Exception as e:
            print(str(e))
            pass

        new_height = driver.execute_script("return window.scrollY;")
        
        # Check if we have reached the end of the page
        if new_height == last_height:
            break
        last_height = new_height

    return all_data


if __name__ == '__main__':

    start = time.time()
    # URL of the data
    url = "https://www.ubereats.com"

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    driver.get(url)

    # Close pop up about auto location (if it appears)
    try:
        elem_close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[title="Close"]'))
            )
        elem_close_button.click()
        time.sleep(2)
    except:
        pass

    # Get 2nd location from the drop down list
    elem = driver.find_element(By.CSS_SELECTOR, 'input[role="combobox"]')
    elem.send_keys("London Ontario Canada")
    time.sleep(2)
    elem.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.5)
    elem.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.5)
    elem.send_keys(Keys.ENTER)
    time.sleep(5)

    # Get all available store links and follow the last in the list
    elems = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="store-card"]')
    links = [elem.get_attribute('href') for elem in elems]
    print(links)

    driver.get(elems[-1].get_attribute('href'))
    time.sleep(5)

    # Get items names and prices
    try:
        menu_items_all = scroll_and_get_all_data(driver, selector="//div[1]/div/span", selector_type=By.XPATH)
        menu_items = [el for el in menu_items_all if el not in [' • ', '']]

        menu_data = []

        for i in range(1, len(menu_items) - 1):
            if '$' in menu_items[i]:
                price = menu_items[i]
                name = menu_items[i-1]
                menu_data.append([name, price])

        with open('menu.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Menu Item', 'Price'])
            writer.writerows(menu_data)

    except Exception as er:
        print(str(er))

    driver.close()
    print('Total time: %s' % str(time.time() - start))