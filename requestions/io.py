# -*- coding: utf-8 -*-
"""
requestions - requests serialization library
"""

import json

try:
    import careful_requests as requests
except ImportError:
    import requests

from .utils import (
    replace_body_with_data,
    delete_blank_keys_from,
    get_and_del_attr,
)

def write_request(obj, return_string=True):
    """
    Serializes a Request to JSON.
    """
    attributes = [
        "body",
        "data", # old versions of requests use "data" instead of "body"
        "method",
        "headers",
        "auth",
        "params",
        "url",
        #"path_url",
        "proxies",
        "config",
    ]

    serialization = {}

    for attribute in attributes:
        if hasattr(obj, attribute):
            serialization[attribute] = getattr(obj, attribute)

    if hasattr(obj, "cookies") and obj.cookies != None:
        serialization["cookies"] = dict(obj.cookies)

    replace_body_with_data(serialization)

    if return_string:
        return json.dumps(serialization)
    elif not return_string:
        return serialization

def write_response(obj, return_string=True):
    """
    Serializes a Response to JSON.
    """
    attributes = [
        "encoding",
        "headers",
        "status_code",
        "url",
        "config",
    ]

    serialization = {}

    for attribute in attributes:
        if hasattr(obj, attribute):
            serialization[attribute] = getattr(obj, attribute)

    if hasattr(obj, "cookies") and obj.cookies != None:
        serialization["cookies"] = dict(obj.cookies)

    serialization["content"] = obj.content

    if hasattr(obj, "request"):
        request = write_request(obj.request, return_string=False)
        serialization["request"] = request

    replace_body_with_data(serialization)

    if return_string:
        return json.dumps(serialization)
    elif not return_string:
        return serialization

def read_request(srequestion):
    """
    Deserializes a Request from JSON.
    """
    kwargs = json.loads(srequestion)
    replace_body_with_data(kwargs)
    delete_blank_keys_from(kwargs)

    if "auth" in kwargs.keys() and kwargs["auth"] != None:
        auth = kwargs["auth"]
        kwargs["auth"] = list(auth)

    requestion = requests.models.Request(**kwargs)

    return requestion

def read_response(srequestion):
    """
    Deserializes a Response from JSON.
    """
    kwargs = json.loads(srequestion)
    delete_blank_keys_from(kwargs)

    attributes = [
        "request",
        "url",
        "status_code",
        "content",
        "headers",
        "cookies",
    ]

    avoid_attributes = [
        "apparent_encoding",
    ]

    for avoidable_attribute in avoid_attributes:
        if avoidable_attribute in kwargs.keys():
            del kwargs[avoidable_attribute]

    temp_store = {}

    for key in attributes:
        value = get_and_del_attr(kwargs, key)
        temp_store[key] = value

    response = requests.models.Response(**kwargs)

    for (key, value) in temp_store.items():
        if key == "content":
            response._content = value
        else:
            setattr(response, key, value)

    if temp_store["request"]:
        request = read_request(json.dumps(temp_store["request"]))
        if request:
            response.request = request

    return response

