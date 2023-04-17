import logging

from automation_core.common.logger import setup_logging
from automation_core.common.retry import retry
from automation_core.ext.driver import wait_and_click, wait_until_element_is_visible
from selenium.webdriver.common.by import By


class HomePage:
    support_btn = "button a[href='#support-heading']"
    api_request_options = ".endpoints li[data-id='{0}'][data-http='{1}']"
    api_request_end_point = "[data-key='request-output-link'] span"
    api_response_code = "[data-key='response-code']"
    api_response_output = "[data-key='output-response']"

    def __init__(self, driver):
        setup_logging()
        self.logger = logging.getLogger(self.__class__.__name__)  # magic dunder
        self.driver = driver

    def verify_home_page_is_displayed(self):
        self.logger.info("verify home page is displayed")
        wait_until_element_is_visible(self.driver, By.CSS_SELECTOR, self.support_btn)

    def click_support_button(self):
        self.logger.info("verify home page is displayed")
        wait_and_click(self.driver, By.CSS_SELECTOR, self.support_btn)

    def send_api_request(self, request_type, end_point):
        self.logger.info("send api request")
        wait_and_click(self.driver, By.CSS_SELECTOR, self.api_request_options.format(end_point, request_type))

    def verify_endpoint_url(self, expected_endpoint):
        self.logger.info("verify endpoint")
        element = wait_until_element_is_visible(self.driver, By.CSS_SELECTOR, self.api_request_end_point)
        assert element.text == expected_endpoint , f"Expected value {element.text} is not equal to actual value {expected_endpoint}"

    @retry()
    def verify_status_code(self, status_code):
        self.logger.info("verify code")
        element = wait_until_element_is_visible(self.driver, By.CSS_SELECTOR, self.api_response_code)
        return element.text == status_code

    def get_api_response(self):
        self.logger.info("verify code")
        element = wait_until_element_is_visible(self.driver, By.CSS_SELECTOR, self.api_response_output)
        return element.text
