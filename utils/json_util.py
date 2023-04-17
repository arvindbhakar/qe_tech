import json
import logging
import os.path

from jsonpath_rw import Index, Fields
from jsonpath_rw_ext import parse

from automation_core.common.logger import setup_logging

setup_logging()
logger = logging.getLogger("json_util")  # magic dunder


def load_json_from_file(file_name):
    logger.info("Check if file exists")
    if os.path.isfile(file_name) is False:
        logger.error("JSON file: " + file_name + " not found")
        raise IOError
    with open(file_name) as json_file:
        data = json.load(json_file)
    return data


def add_object_to_json(json_object, json_path, object_to_add):
    json_path_expr = parse(json_path)
    for match in json_path_expr.find(json_object):
        if type(match.value) is dict:
            match.value.update(object_to_add)
        if type(match.value) is list:
            match.value.append(object_to_add)

    return json_object


def get_value_from_json(json_object, json_path):
    json_path_expr = parse(json_path)
    return [match.value for match in json_path_expr.find(json_object)]


def update_value_to_json(json_object, json_path, new_value):
    json_path_expr = parse(json_path)
    for match in json_path_expr.find(json_object):
        path = match.path
        if isinstance(path, Index):
            match.context.value[match.path.index] = new_value
        elif isinstance(path, Fields):
            match.context.value[match.path.fields[0]] = new_value
    return json_object


def update_multi_record_json(json_object, json_path, new_value=[]):
    json_path_expr = parse(json_path)
    i = 0
    for match in json_path_expr.find(json_object):
        path = match.path
        if isinstance(path, Index):
            match.context.value[match.path.index] = new_value[i]
        elif isinstance(path, Fields):
            match.context.value[match.path.fields[0]] = new_value[i]
        i+=1
    return json_object


def delete_object_from_json(json_object, json_path):
    json_path_expr = parse(json_path)
    for match in json_path_expr.find(json_object):
        path = match.path
        if isinstance(path, Index):
            del (match.context.value[match.path.index])
        elif isinstance(path, Fields):
            del (match.context.value[match.path.fields[0]])
    return json_object


def convert_json_to_string(json_object):
    return json.dumps(json_object)


def convert_string_to_json(json_string):
    return json.loads(json_string)
