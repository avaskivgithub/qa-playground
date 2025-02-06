import time
import random
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import bot_alert
import os

script_dir_path = os.path.dirname(os.path.abspath(__file__))

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Bot(object):

    def __init__(self, profiles_list_file_path, filter_words_list_file_path):
        self.bot = bot_alert.BotAlert(bot_token=None) # TOBD: add reading token from environment variables
        self.chat_id = '-4706647839'

        df = pd.read_csv(profiles_list_file_path)
        self.profiles_list = df.iloc[:, 0].to_list()
        logging.info("Loaded Profiles into %s" % profiles_list_file_path)

        df = pd.read_csv(filter_words_list_file_path)
        self.filter_words_list = df.iloc[:, 0].to_list()
        logging.info("Loaded Profiles into %s" % filter_words_list_file_path)

    def lookup_profile_and_alert(self, driver, profile):
        try:
            # Scrap the page
            filtered_posts_dict = driver.scrape_page_and_filter_out_posts(profile, self.filter_words_list)

            # Alert only if there is anything
            filtered_posts_list, url = filtered_posts_dict['posts'], filtered_posts_dict['url']
            if filtered_posts_list:
                filtered_posts_list.insert(0, 'SOURCE: %s \nFollowing Lookup Results:' % url)
                self.bot.send_message(chat_id=self.chat_id, msg='\n\n - '.join(filtered_posts_list))

        except Exception as e:
            logging.error('while reading profile %s: %s' % (profile, str(e)))
            pass

    def run(self):
        with WebScrapingTwitterProfile() as web_page_scraper_driver:
            for profile in self.profiles_list:
                self.lookup_profile_and_alert(web_page_scraper_driver, profile)

class WebScrapingTwitterProfile(object):

    def __init__(self):

        self.url_template = 'https://x.com/%s?mx=2'

        # Selenium
        self.driver = None
        self.options = Options()
        self.options.headless = True

        # CSS Selectors
        self.selectors = ['div[data-testid="primaryColumn"]', 'div[data-testid="tweetText"]', 'span.css-1jxf684', 'a[role="link"]']
        self.selector_post_time = 'time[datetime]'

    def __enter__(self):
        logging.info(f"Start scraping")

        # Set random proxy
        cmnt = """
        proxy_list = [
            {"http": "103.160.150.251:8080", "https": "103.160.150.251:8080"},
            {"http": "38.65.174.129:80", "https": "38.65.174.129:80"},
            {"http": "46.105.50.251:3128", "https": "46.105.50.251:3128"},
        ]
        proxies = proxy_list[random.randint(0, len(proxy_list)-1)]
        proxy_settings = Proxy()
        
        proxy_settings.proxy_type = ProxyType.MANUAL
        proxy_settings.http_proxy = proxies["http"]
        proxy_settings.ssl_proxy = proxies["https"]
        
        capabilities = webdriver.DesiredCapabilities.FIREFOX
        proxy_settings.add_to_capabilities(capabilities)
        """
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=self.options)
                                        # desired_capabilities=capabilities)
        return self  # Return the instance to use within the with block

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver = None
        logging.info(f"Stop scraping")
        # If any exception occurs, you can choose to handle it here
        # Return False to propagate the exception, True to suppress it
        return False

    def scrape_page_and_filter_out_posts(self, profile, filter_words_list=None):
        
        driver, url = self.driver, self.url_template % profile
        selector_page_loaded, selectors = self.selector_post_time, self.selectors

        # Initialize set for collected posts
        all_posts = {" "}

        # Open page
        driver.get(url)
        logging.info('URL: %s' % url)

        # Wait for page to load
        try:
            el_page_loaded = WebDriverWait(driver, 1000).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector_page_loaded))
                )
            logging.info("%s: Page loaded %s" % (url, el_page_loaded.text))
        except Exception as e:
            logging.warning("%s: %s" % (url, str(e)))
            pass

        # Initialize data in pixels for scrolling
        step_height = driver.execute_script("return window.innerHeight;")
        logging.info('%s: view port height %s' % (url, step_height))
        last_height = driver.execute_script("return window.scrollY;")
        logging.info("%s: The initial scroll height %s" % (url, last_height))

        # Start collecting data from the page
        while True:
            try:
                for selector in selectors:
                    elems = driver.find_element(By.CSS_SELECTOR, selector)
                    list = elems.text.split('\n')
                    all_posts.update(list)

                # Scroll down by view port height
                driver.execute_script("window.scrollBy({ top: %s });" % step_height) 
                driver.implicitly_wait(2)
            except Exception as e:
                print(str(e))
                pass

            new_height = driver.execute_script("return window.scrollY;")
            logging.debug('%s: page scrolled to  %s' % (url, new_height))
            
            # Check if we have reached the end of the page
            if new_height == last_height:
                break
            last_height = new_height

        logging.info('%s: total posts  %s' % (url, len(all_posts)))
        filtered_posts_list = [elem for elem in all_posts if any(filter_word in elem.lower() for filter_word in filter_words_list)]
        logging.info('%s: total filtered posts  %s' % (url, len(filtered_posts_list)))

        return {'posts': filtered_posts_list, 'url': url}

def generate_csv_test_list_of_public_profiles(file_path):

    url_most_followed_accounts_list = 'https://en.wikipedia.org/wiki/Template:List_of_most-followed_Twitter_accounts'
    logging.info("For Testing Profiles Read %s" % url_most_followed_accounts_list)
    tables = pd.read_html(url_most_followed_accounts_list)
    profile_list = [el.lower() 
                for el in tables[0]["Username"].str.replace('@', '')
                if not any(c.isspace() for c in el)]
    
    logging.info("Store Profiles into %s" % file_path)
    df = pd.DataFrame(profile_list, columns=['ProfileUsername'])
    df.to_csv(file_path, index=False)

    return profile_list

if __name__ == "__main__":

    start = time.time()

    file_path_profiles_list = os.path.join(script_dir_path, 'public_profiles.csv')
    file_path_lookup_words = os.path.join(script_dir_path, 'bot_lookup_words.csv')
    # generate_csv_test_list_of_public_profiles(file_path_profiles_list)

    # Run bot for all profiles from file_path_profiles_list
    bot_xplatform = Bot(file_path_profiles_list, file_path_lookup_words)
    bot_xplatform.run()

    # Calculate the elapsed time
    elapsed_time = time.time() - start
    print(f"Elapsed time: {elapsed_time:.2f} seconds")