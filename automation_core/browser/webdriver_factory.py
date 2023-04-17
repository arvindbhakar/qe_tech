import logging
import os
from pathlib import Path
from typing import Union

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.firefox.service import Service as FireFoxService
from selenium.webdriver.firefox.webdriver import WebDriver as FireFoxDriver
from selenium.webdriver.ie.webdriver import WebDriver as IEDriver
from webdriver_manager.chrome import ChromeDriverManager  # type: ignore
from webdriver_manager.core.utils import ChromeType  # type: ignore
from webdriver_manager.firefox import GeckoDriverManager  # type: ignore
#from webdriver_manager.utils import ChromeType

from automation_core.common.logger import setup_logging


def get_download_directory() -> str:
    base_dir = str(Path.cwd()).split(os.path.sep, maxsplit=1)[0] + os.path.sep
    return str(base_dir) + "auto_download"


class WebDriverFactory:
    WebDriverObject = Union[FireFoxDriver, ChromeDriver, IEDriver, None]

    def __init__(self) -> None:
        setup_logging()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.browser = str(os.getenv("BROWSER_TYPE", "chromium"))
        self.is_headless = os.getenv("HEADLESS_MODE", "False")

    def get_web_driver(self) -> WebDriverObject:
        if self.browser == "firefox":
            ff_options = self.set_firefox_options()
            path = GeckoDriverManager().install()
            return FireFoxDriver(service=FireFoxService(path), options=ff_options)
        if self.browser == "chromium":
            chrome_options = self.set_chrome_options()
            chrome_options.binary_location = os.getenv("TA_CHROME_OPTION_STR_BinaryLocation", "")
            chrome_driver = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            return ChromeDriver(service=ChromeService(chrome_driver), options=chrome_options)
        if self.browser == "chrome":
            chrome_options = self.set_chrome_options()
            chrome_driver = ChromeDriverManager().install()
            return ChromeDriver(service=ChromeService(chrome_driver), options=chrome_options)

        self.logger.error("Invalid browser type: %s", self.browser)
        raise ValueError(f"Invalid browser type: {self.browser}")

    @staticmethod
    def initialize_webdriver() -> WebDriverObject:
        wdf = WebDriverFactory()
        driver = wdf.get_web_driver()
        return driver

    def quit_webdriver(self, driver: WebDriverObject) -> None:
        try:
            if driver is not None:
                driver.quit()
                driver = None
        except Exception as exception:
            self.logger.error("When closing browser, received exception: %s", exception)
            raise exception

    def set_chrome_options(self) -> ChromeOptions:
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--test-type")
        if self.is_headless == "True":
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('window-size=1920x1080')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.add_experimental_option("prefs", {
        #     "download.default_directory": self.chrome_download,
        #     "download.prompt_for_download": False,
        #     "download.directory_upgrade": True,
        #     "safebrowsing.enabled": False,
        #     "safebrowsing_for_trusted_sources_enabled": False
        # })
        self.logger.debug("Chrome options are: %s", chrome_options)
        return chrome_options

    def set_firefox_options(self) -> FireFoxOptions:
        options = FireFoxOptions()
        options.add_argument("--ignore-certificate-errors")
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        download_dir = get_download_directory()
        options.set_preference("browser.download.dir", download_dir)
        file_list = "text/csv,application/x-msexcel,application/excel," \
                    "application/x-excel,application/vnd.ms-excel," \
                    "image/png,image/jpeg,text/html,text/plain,application/msword,application/xml"
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", file_list)
        if self.is_headless == "True":
            options.add_argument("--headless")
        self.logger.debug("Firefox options are: %s", options)
        return options
