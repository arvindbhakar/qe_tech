from behave import *

from page_objects.support_page import SupportPage


@then('Verify support page is displayed')
def step_impl(context):
    sp = SupportPage(context.driver)
    sp.verify_support_page_is_displayed()


@then('Verify one time support option is displayed')
def step_impl(context):
    sp = SupportPage(context.driver)
    sp.verify_one_time_support_option_is_displayed()


@then('Verify monthly support option is displayed')
def step_impl(context):
    sp = SupportPage(context.driver)
    sp.verify_monthly_support_option_is_displayed()
