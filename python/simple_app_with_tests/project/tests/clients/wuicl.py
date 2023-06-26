#!/usr/bin/python

import re
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)

from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import NoSuchElementException


class WUI(object):
    """
        Wrapper for webdriver calls.
    """
    def __init__(self, profile=FirefoxOptions(), wait_timeout=5):

        # profile.set_preference("webdriver_enable_native_events", False)
        self.driver = webdriver.Firefox(options=profile)
        self.driver.implicitly_wait(30)

    # =============== Page Properties / Elements ============

    def html(self):
        """Current page source."""
        return self.driver.page_source

    def url(self):
        """Current page url."""
        return self.driver.current_url

    def soup(self):
        """Current page soup."""
        return BeautifulSoup(self.html(), "html.parser")

    def get_element(self, by, element_name):
        """Return element-locator

        - by: Type of element-locator. css, xpath, name, id, etc...
        - element_name: Element-locator's name.
        """
        try:
            el = self.driver.find_element(by=by, value=element_name)
        except NoSuchElementException:
            el = None

        return el

    def wait_element_present(self, element_type, element_name, wait_timeout=5):
        """Raise exception if element-locator is not present on page.

        - element_type: Type of element-locator. css, xpath, name, id, etc...
        - element_name: Element-locator's name.
        """
        wait = ui.WebDriverWait(self.driver, timeout=wait_timeout)

        message = '"{}: {}" was not found on page "{}".'.format(element_type, element_name, self.url())
        wait.until(lambda driver: driver.find_element(element_type, element_name),
                    message=message)

    # =============== Page Open / Close ==================

    def open_page(self, url):

        logging.debug('Opening page "{}"'.format(url,))
        self.driver.get(url)

    def close(self):
        """Close browser"""
        self.driver.close()

    # =============== Page Elements' Operations ============

    def get_table_content_by_name(self, name):

        bs = self.soup()
        table = bs.find(lambda tag: tag.name == 'table' and tag.has_attr('name') and tag['name'] == name)

        data_rows = []
        for line in table.findAll('tr'):
            row = []

            # For header
            for cel in line.findAll('th'):
                row.append(cel.getText())

            # For data row
            for cel in line.findAll('td'):
                row.append(cel.getText())

            data_rows.append(row)

        return data_rows

    def click_button(self, element_name, element_type='name'):
        """Click button.

        - element_name: Element-locator's name.
        - element_type: Type of element-locator. css, xpath, name, id, etc.

        """
        logging.debug('Clicking button "{}: {}" on "{}".'.format(
                          element_type, element_name, self.url()))

        # Get the element and click
        self.wait_element_present(element_type, element_name, wait_timeout=1)
        element = self.get_element(by=element_type, element_name=element_name)

        element.click()

    def fill_in_text_field(self, element_name, text, element_type='name'):
        """Clear and fill in text input / area with specified text.

        - element_name: Element-locator's name.
        - text: Text value.
        - element_type: Type of element-locator. css, xpath, name, id, etc.

        """
        logging.debug('Filling in text field "{}: {}" on "{}" with text "{}"'.format(
                          element_type, element_name, self.url(), text))

        # Get the element and fill in data
        self.wait_element_present(element_type, element_name, wait_timeout=1)
        element = self.get_element(by=element_type, element_name=element_name)

        element.clear()
        element.send_keys(text)

if __name__ == '__main__':

    browser = WUI()
    browser.open_page('http://127.0.0.1:5000')
    browser.wait_element_present('name', 'deleteAllTests')
    browser.click_button('addTest')
    browser.close()

# EOF
