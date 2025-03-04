"""
README: Function `ask_ai_chat` opens https://copilot.microsoft.com/chats.
        Enters prompt question.
        Waits `wait_response` (7 seconds by default).
        Copies the response and returns it. 

        If you are not ready to sign up for real AI API (no good use case to try it out), 
        but you want to have experience calling it.

To test out IMAGE COMPARISON:
        - `compare_images` function added
        - to the `ask_ai_chat` function was added taking screenshot based on the TAKE_SCREENSHOT_EXPECTED flag
          and calling `compare_images` function to generate highlighted_differences_chat_ai_screenshot.png

To test out FILES COMPARISON `diff_files` and `compare_chat_ai_text_responses` functions were added
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from PIL import Image, ImageChops, ImageDraw

import time
import os
import difflib

script_dir_path = os.path.dirname(os.path.abspath(__file__))

expected_file_name_prefix = 'expected_'
highlighted_differences_file_name_prefix = 'highlighted_differences_'
screenshot_file_name = 'chat_ai_screenshot.png'
text_response_file_name = 'response_output.txt'

def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f"Total time '{func.__name__}' took: {time.time() - start_time:.4f} seconds")
        return result
    return wrapper

def compare_images(image1_path, image2_path):
    result_similar = False

    # Open the images
    img1 = Image.open(image1_path).convert("RGB")
    img2 = Image.open(image2_path).convert("RGB")

    # Check if images have the same size
    if img1.size != img2.size:
        print("Images have different dimensions and cannot be compared.")
        
    # Compute the difference
    diff = ImageChops.difference(img1, img2)

    # Highlight differences
    diff_highlight = img1.copy()
    draw = ImageDraw.Draw(diff_highlight)

    # Get the bounding box of the differences
    diff_bbox = diff.getbbox()
    if diff_bbox:
        draw.rectangle(diff_bbox, outline="red", width=5)  # Mark the difference area

    # Check if the images are identical
    if diff.getbbox() is None:
        print("The images are identical.")
        result_similar = True
    else:
        print("The images are different.")
        # diff.show()  # Display the difference image

    # Save the output image
    output_path = os.path.join(script_dir_path, f'{highlighted_differences_file_name_prefix}{screenshot_file_name}')
    diff_highlight.save(output_path)
    print(f"Difference image saved as: {output_path}")

    return result_similar

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
        # 1. Enter question
        elem = WebDriverWait(driver, 1000).until(
                EC.presence_of_element_located((By.ID, 'userInput'))
                )
        
        elem.send_keys(question)
        elem.send_keys(Keys.ENTER)
        time.sleep(wait_response)

        # 2. Click Copy response
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        button = WebDriverWait(driver, 1000).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'button[title="Copy message"]'))
                )
        
        button.click()
        elem.send_keys(" ")

        # 3. Take a snapshot and compare with expected file
        expected_file_path = os.path.join(script_dir_path, f'{expected_file_name_prefix}{screenshot_file_name}')
        actual_file_path = os.path.join(script_dir_path, screenshot_file_name)

        action = ActionChains(driver)
        driver.save_screenshot(actual_file_path)
        if not os.path.exists(expected_file_path):
            driver.save_screenshot(expected_file_path)

        similar = compare_images(actual_file_path, expected_file_path)
        print(similar)
        
        # 4. Paste copied response via pressing CTRL+V
        action.key_down(Keys.CONTROL).send_keys('V').key_up(Keys.CONTROL).perform()
        response = elem.text

    except Exception as er:
        print(str(er))

    driver.close()
    return response

def diff_files(file1_path, file2_path, output_path=None):
    # Read the contents of the files
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        file1_lines = file1.readlines()
        file2_lines = file2.readlines()

    # Compute the differences
    diff = difflib.unified_diff(
        file1_lines,
        file2_lines,
        fromfile='File1',
        tofile='File2',
        lineterm=''
    )

    # Output the differences
    diff_output = '\n'.join(diff)
    if output_path:
        with open(output_path, 'w') as output_file:
            output_file.write(diff_output)
        print(f"Differences saved to: {output_path}")
    else:
        print("Differences:")
        print(diff_output)

def compare_chat_ai_text_responses(response):
    file_path_with_expected_response = os.path.join(script_dir_path, f"{expected_file_name_prefix}{text_response_file_name}")
    file_path_with_response = os.path.join(script_dir_path, text_response_file_name)
    file_path_with_differences = os.path.join(script_dir_path, f'{highlighted_differences_file_name_prefix}{text_response_file_name}')

    if not os.path.exists(file_path_with_expected_response):
        # Just save response to the file_path_with_expected_response if it doesn't exist
        with open(file_path_with_expected_response, "w") as exp_file:
            exp_file.write(response)

    # Save response to the file_path_with_response and compare with file_path_with_expected_response
    with open(file_path_with_response, "w") as file:
        file.write(response)
    diff_files(file_path_with_expected_response, file_path_with_response, file_path_with_differences)

if __name__ == '__main__':

    # TALK to the chat ai and get response
    response = ask_ai_chat(question="Python script that save data into file",
                        wait_response=5)

    # COMPARE text responses
    compare_chat_ai_text_responses(response)
