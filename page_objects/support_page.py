import logging

from automation_core.common.logger import setup_logging
from automation_core.ext.driver import wait_and_click, wait_until_element_is_visible
from selenium.webdriver.common.by import By


class SupportPage:
    support_page = ".pro#support"
    one_time_support_option = "#supportOneTime"
    monthly_support_option = "#supportRecurring"

    def __init__(self, driver):
        setup_logging()
        self.logger = logging.getLogger(self.__class__.__name__)  # magic dunder
        self.driver = driver

    def verify_support_page_is_displayed(self):
        self.logger.info("verify support page is displayed")
        wait_until_element_is_visible(self.driver, By.CSS_SELECTOR, self.support_page)

    def verify_one_time_support_option_is_displayed(self):
        self.logger.info("verify_one_time_support_option_is_displayed")
        wait_until_element_is_visible(self.driver, By.CSS_SELECTOR, self.one_time_support_option)

    def verify_monthly_support_option_is_displayed(self):
        self.logger.info("verify_monthly_support_option_is_displayed")
        wait_until_element_is_visible(self.driver, By.CSS_SELECTOR, self.monthly_support_option)