from behave import *

from page_objects.home_page import HomePage
from page_objects.support_page import SupportPage
from utils.json_util import convert_string_to_json, get_value_from_json


@then("Response contains user id '{id}'")
def step_impl(context, id):
    hp = HomePage(context.driver)
    res = hp.get_api_response()
    json_obj = convert_string_to_json(res)
    actual_id = get_value_from_json(json_obj, "$.data.id")
    assert actual_id, id

@then("Response contains user name as '{value}'")
def step_impl(context, value):
    hp = HomePage(context.driver)
    res = hp.get_api_response()
    json_obj = convert_string_to_json(res)
    actual_name = get_value_from_json(json_obj, "$.name")
    assert actual_name, value