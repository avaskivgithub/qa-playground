import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
import time

# URL of the data
url = "https://www.derive.xyz/options/btc"
driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.get(url)
time.sleep(10) # proper implicit timeout needed

# Close the pop up window
selector = '//*[@id="content-:r58:"]/div'
elem = driver.find_element(By.XPATH, selector)
button = driver.find_element(By.XPATH, '//*[@id="content-:r58:"]/div/div[1]/div[2]/span/button')
button.click()
time.sleep(10) # proper implicit timeout needed

# Get all columns names
selector_clmns = '//*[@id="root"]/div[3]/div/div[1]/div[2]/div/div/div[2]/div/div/div[1]/div[2]'
elems_clmns = driver.find_element(By.XPATH,selector_clmns)
columns = elems_clmns.text.split('\n')
print(columns)

# Now let's read rows
selector_row = '//*[@id="root"]/div[3]/div/div[1]/div[2]/div/div/div[2]/div/div/div[%s]'
selector_data = selector_row + '/div[%s]'
matrix =[]
row_still_exists = True
row_count = 1
while row_still_exists:
    
    # make sure next row exists
    try:
        row_count += 1
        driver.find_element(By.XPATH, selector_row % row_count)
    except NoSuchElementException as er:
        row_still_exists = False
        print(str(er))

    # iterating through the row
    try:
        data = []
        for i in range(1, len(columns)+1):
            selector_i = selector_data % (row_count, i)
            elem_data = driver.find_element(By.XPATH,selector_i)
            data.append(elem_data.text)
        matrix.append(data)
    except NoSuchElementException as er:
        print(str(er))
        # ignore rows with sum data
        pass
        
# Convert to DataFrame
df = pd.DataFrame(matrix, columns=columns)

# Display DataFrame
print(df)

driver.close()
