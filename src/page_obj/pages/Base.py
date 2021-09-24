import time

from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.webdriver.support.ui import Select

from src.page_obj.Locators import Locator


class BasePage(object):

    def __init__(self, driver: EventFiringWebDriver):
        self.driver = driver
        self.MARKET_LINK = "Market"
        self.MY_CART_LINK = "My Cart"

    def go_to_url(self, url):
        self.driver.get(url)

    def click_link_by_text(self, text):
        print('Clicking ', text, ' link.')
        self.driver.find_element_by_xpath(Locator.link_by_text.format(link_text=text)).click()

    def send_text_by_placeholder(self, placeholder, text):
        print('Entering text ', text, ' into field with placeholder ', placeholder)
        ele = self.driver.find_element_by_xpath(Locator.input_by_placeholder.format(placeholder_text=placeholder))
        self.slow_type(ele, text)

    def send_text_by_section_and_label(self, section, label, text):
        print('Entering text ', text, ' to field in section ', section, ' with label ', label)
        ele = self.driver.find_element_by_xpath(Locator.input_by_section_and_label
                                                .format(section_text=section, label_text=label))
        self.slow_type(ele, text)

    def select_dropdown_by_section_and_label(self, section, label, text):
        ele = self.driver.find_element_by_xpath(Locator.select_by_section_and_label
                                                .format(section_text=section, label_text=label))
        select = Select(webelement=ele)
        select.select_by_visible_text(text)

    def select_dropdown_by_section_label_count(self, section, label, count, text):
        ele = self.driver.find_element_by_xpath(Locator.select_by_section_and_label
                                                .format(section_text=section, label_text=label) + '[' + str(
            count) + ']')
        select = Select(webelement=ele)
        select.select_by_visible_text(text)

    def select_dropdown_by_index(self, section, label, count, index):
        ele = self.driver.find_element_by_xpath(Locator.select_by_section_and_label
                                                .format(section_text=section, label_text=label) + '[' + str(
            count) + ']')
        select = Select(webelement=ele)
        select.select_by_index(index)

    def click_checkbox_by_label(self, text):
        self.driver.find_element_by_xpath(Locator.checkbox_by_label.format(label_text=text)).click()

    def navigate_back(self):
        self.driver.back()

    # Artificially slow typing for FS capture
    def slow_type(self, element, text):
        for char in text:
            element.send_keys(char)
            time.sleep(.1)

