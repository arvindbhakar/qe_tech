from time import sleep

from behave import *

from page_objects.home_page import HomePage


@given('Home page is open')
def login_application(context):
    hp = HomePage(context.driver)
    hp.verify_home_page_is_displayed()


@when('API request {requestType} is send with {endpoint}')
def step_impl(context, requestType, endpoint):
    hp = HomePage(context.driver)
    hp.send_api_request(requestType, endpoint)


@then("Verify '{endpoint_url}' is displayed")
def step_impl(context, endpoint_url):
    hp = HomePage(context.driver)
    hp.verify_endpoint_url(endpoint_url)


@then("Verify status is '{code}'")
def step_impl(context, code):
    hp = HomePage(context.driver)
    hp.verify_status_code(code)


@when('Click on support button')
def step_impl(context):
    hp = HomePage(context.driver)
    hp.click_support_button()
