"""
README: 
        1. collect data from UberEats restaurant pages (for now just 1 page)
        2. get Menu Items: Names, Prices
        3. the result saved into menu.csv
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
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
    # url = "https://www.ubereats.com/ca/collection-page?collectionName=ca-foodflavors-chocolate"
    # url = "https://www.ubereats.com/ca/store/rades-restaurant/PLu8iobhUb6WCGNzZqVfWQ?diningMode=DELIVERY"
    url = "https://www.ubereats.com/store/aloy-thai-cuisine/WceXtnnCRNSIoixZqneUqg?diningMode=DELIVERY"
    # url = "https://www.ubereats.com/ca/store/mcdonalds-northfield-%26-davenport/PmeLkXqMTJargw2CByApjQ?diningMode=DELIVERY"

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    driver.get(url)
    time.sleep(3) # proper implicit timeout needed

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