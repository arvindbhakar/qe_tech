from typing import List, Union
from typing import Any, Optional

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from automation_core.common.retry import retry


def wait_and_click(
    driver: WebDriver, by: By, locator: str, timeout: int = 30
) -> None:
    @retry(timeout=timeout)
    def _click_web_element() -> bool:
        driver.find_element(by, locator).click()
        return True

    _click_web_element()




def find_clickable_elements(driver: WebDriver,
                            by: By, locator: str) -> List[WebElement]:
    elements = list(filter(lambda x: (x.is_displayed() and x.is_enabled()),
                           driver.find_elements(by, locator)))
    if elements is None:
        raise NoSuchElementException("No clickable (visible and enabled) element found!")
    return elements


def find_clickable_element(driver: WebDriver, by: By, locator: str) -> WebElement:
    elements = driver.find_elements(by, locator)
    element = next((e for e in elements if e.is_displayed() and e.is_enabled()), None)
    if element is None:
        raise NoSuchElementException("No clickable (visible and enabled) element found!")
    return element


def find_visible_element(driver: WebDriver, by: By, locator: str) -> WebElement:
    elements = driver.find_elements(by, locator)
    visible_element = next((e for e in elements if e.is_displayed()), None)
    if visible_element is None:
        raise NoSuchElementException("No visible child-element found!")
    return visible_element


def find_visible_elements(driver: WebDriver, by: By, locator: str) -> List[WebElement]:
    elements = driver.find_elements(by, locator)
    return list(filter(lambda x: x.is_displayed(), elements))





def is_element_visible(driver: WebDriver, by: By, locator: str) -> Union[WebElement, bool]:
    try:
        return find_visible_element(driver, by, locator)
    except StaleElementReferenceException:
        return is_element_visible(driver, by, locator)
    except Exception:
        return False


def is_element_enabled(driver: WebDriver, by: By, locator: str) -> bool:
    try:
        return driver.find_element(by, locator).is_enabled()
    except StaleElementReferenceException:
        return is_element_enabled(driver, by, locator)
    except Exception:
        return False


def is_element_present_in_dom(driver: WebDriver, by: By, locator: str) -> bool:
    return len(driver.find_elements(by, locator)) > 0


def is_element_clickable(driver: WebDriver, by: By, locator: str) -> bool:
    try:
        find_clickable_element(driver, by, locator)
        return True

    except NoSuchElementException:
        return False

    except StaleElementReferenceException:
        return is_element_clickable(driver, by, locator)


def wait_until_element_present_in_dom(driver: WebDriver, by: By,
                                      locator: str, timeout: int = 30) -> Any:
    @retry(timeout=timeout)
    def _wait_for_element() -> Any:
        return driver.find_element(by, locator)

    return _wait_for_element()


@retry()
def wait_until_element_is_not_present_in_dom(driver: WebDriver, by: By, locator: str) -> bool:
    return not is_element_present_in_dom(driver, by, locator)


def wait_until_element_is_visible(driver: WebDriver, by: By, locator: str,
                                  timeout: int = 60) -> Any:
    @retry(timeout=timeout)
    def _wait_for_element() -> Any:
        return find_visible_element(driver, by, locator)

    return _wait_for_element()


def wait_until_element_is_not_visible(driver: WebDriver, by: By, locator: str,
                                      timeout: int = 60) -> Any:
    @retry(timeout=timeout)
    def _wait_no_element() -> bool:
        try:
            element = driver.find_element(by, locator)
            return not element.is_displayed()
        except (NoSuchElementException, StaleElementReferenceException):
            return True

    return _wait_no_element()


def wait_until_element_is_clickable(driver: WebDriver, by: By, locator: str,
                                    timeout: int = 60) -> Any:
    @retry(timeout=timeout)
    def _wait_for_clickable_element() -> WebElement:
        return find_clickable_element(driver, by, locator)

    return _wait_for_clickable_element()


def wait_until_element_at_index_exists(driver: WebDriver, by: By, locator: str,
                                       index: int, timeout: int = 30) -> Any:
    @retry(timeout=timeout)
    def _wait_for_element() -> Any:
        elements = driver.find_elements(by, locator)
        if len(elements) > index:
            return elements[index]

        return None

    return _wait_for_element()


def wait_until_text_node_equals(driver: WebDriver, by: By, locator: str,
                                expected: str, timeout: int = 60) -> None:
    @retry(timeout=timeout)
    def _wait_for_equal_nodes() -> bool:
        print("wait until note equals")
        element_text_value = find_visible_element(driver, by, locator).text
        if element_text_value == expected:
            return True

        raise ValueError("The actual UI value (" + element_text_value +
                         ") and the expected value (" + expected + ") do no match!")

    _wait_for_equal_nodes()
