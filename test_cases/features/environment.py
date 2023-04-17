import base64
import os

import allure
from behave import *

from automation_core.browser.browser import Browser
from test_cases.config import QE_TECH_URL


@fixture
def open_application(context):
    context.browser = Browser(url=QE_TECH_URL)
    context.driver = context.browser.driver
    context.browser.maximize_window()
    yield
    context.browser.quit_driver()


def before_scenario(context, feature):
    use_fixture(open_application, context)


def after_step(context, step):
    if step.status.name == 'failed':
        if "allure_behave.formatter:AllureFormatter" in context._config.format:
            allure.attach(context.driver.get_screenshot_as_png(), name="Screenshot",
                          attachment_type=allure.attachment_type.PNG)


def after_scenario(context, scenario):
    try:
        stdout = context.stdout_capture.getvalue()
        stderr = context.stderr_capture.getvalue()
        if stdout:
            allure.attach(stdout, name="stdout", attachment_type=allure.attachment_type.TEXT)
        if stderr:
            allure.attach(stderr, name="stderr", attachment_type=allure.attachment_type.TEXT)
    except:
        pass
    if scenario.status.name != 'passed':
        screen_shot_dir = os.path.join(os.getcwd(), "screenshots")
        if not os.path.exists(screen_shot_dir):
            os.makedirs(screen_shot_dir)
        img = os.path.join(screen_shot_dir, f"{context.scenario.name[:100]}...scn.png")
        context.browser.save_web_page(img)
        with open(img, "rb") as f:
            allure.attach(f.read(), name=img, attachment_type=allure.attachment_type.PNG)
    context.browser.quit_driver()
