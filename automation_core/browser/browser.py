import logging
from pathlib import Path
from traceback import print_stack
from typing import List, Any

from selenium.webdriver.remote.webdriver import WebDriver

from automation_core.browser.webdriver_factory import WebDriverFactory
from automation_core.common.logger import setup_logging
from automation_core.common.retry import retry


class Browser:
    def __init__(self, driver: WebDriver = None, implicit_wait: int = 30, url: str = "") -> None:
        setup_logging()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.driver = driver
        if driver is None:
            self.logger.info("Launching Driver in Browser")
            wdf = WebDriverFactory()
            self.driver = wdf.get_web_driver()
        self.set_implicit_wait(implicit_wait)
        if url != "":
            self.navigate_to_url(url)

    def set_implicit_wait(self, implicit_wait: int = 30) -> None:
        self.logger.info("implicitly wait is %s", implicit_wait)
        self.driver.implicitly_wait(implicit_wait)

    def maximize_window(self) -> None:
        self.logger.info("maximizing window")
        self.driver.maximize_window()

    @retry()
    def navigate_to_url(self, url: str) -> bool:
        self.logger.info("navigate to url %s", url)
        self.driver.get(url)
        return True

    def quit_driver(self) -> None:
        self.logger.info("quitting driver")
        try:
            if self.driver is not None:
                self.driver.quit()
                self.driver = None
        except Exception as exception:
            self.logger.error("When closing browser, received exception: %s", exception)
            raise exception

    def close_window(self) -> None:
        self.logger.info("closing current window")
        count = self.get_window_count()
        self.logger.info("total windows count %s", count)
        if count == 1:
            self.quit_driver()
        else:
            self.driver.close()
            window = self.get_all_windows()[-1]
            self.switch_to_window(window)

    def save_web_page(self, file: Path) -> None:
        try:
            self.driver.get_screenshot_as_file(file)
            self.logger.info("Screenshot save to directory: %s", file)
        except IOError as io_error:
            self.logger.error("Exception Occurred when taking screenshot %s", io_error)
            print_stack()

    def save_page_source(self, html_file: Path) -> None:
        try:
            html_content = self.driver.page_source

            with open(html_file, "w", encoding="utf-8") as file:
                file.write(str(html_content))
                self.logger.info("page source save to directory: %s", html_file)
        except Exception as exception:
            self.logger.error("Exception Occurred when getting page source %s", exception)
            print_stack()

    def get_web_page_as_png(self) -> bytes:
        return self.driver.get_screenshot_as_png()
