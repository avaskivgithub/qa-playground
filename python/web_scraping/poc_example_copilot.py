"""
README: Function `ask_ai_chat` opens https://copilot.microsoft.com/chats.
        Enters prompt question.
        Waits `wait_response` (7 seconds by default).
        Copies the response and returns it. 

        If you are not ready to sign up for real AI API (no good use case to try it out), 
        but you want to have experience calling it.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f"Total time '{func.__name__}' took: {time.time() - start_time:.4f} seconds")
        return result
    return wrapper

@time_decorator
def ask_ai_chat(question, wait_response=7):
    # URL of the data
    url = "https://copilot.microsoft.com/chats"
    response = ""

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    driver.get(url)

    try:
        elem = WebDriverWait(driver, 1000).until(
                EC.presence_of_element_located((By.ID, 'userInput'))
                )
        
        elem.send_keys(question)
        elem.send_keys(Keys.ENTER)
        time.sleep(wait_response)

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        button = WebDriverWait(driver, 1000).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[title="Copy message"]'))
                )
        
        button.click()
        elem.send_keys(" ")

        # Take a snapshot
        action = ActionChains(driver)
        driver.save_screenshot('chat_ai_screenshot.png')
        
        # perform the operation
        action.key_down(Keys.CONTROL).send_keys('V').key_up(Keys.CONTROL).perform()

        response = elem.text

    except Exception as er:
        print(str(er))

    driver.close()
    return response

if __name__ == '__main__':

    response = ask_ai_chat(question="Python script that save data into file",
                        wait_response=5)

    # Open a file in write mode
    with open("output.txt", "w") as file:
        # Write data to the file
        file.write(response)