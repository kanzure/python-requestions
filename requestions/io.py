# -*- coding: utf-8 -*-
"""
requestions - requests serialization library
"""

import json

import requests

from .utils import (
    replace_body_with_data,
    delete_blank_keys_from,
    convert_to_dict,
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
        return json.dumps(convert_to_dict(serialization))
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
        return json.dumps(convert_to_dict(serialization))
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

    response = requests.models.Response()

    for (key, value) in kwargs.items():
        if key == "content":
            response._content = value
        elif key == "request":
            request = read_request(json.dumps(value))
            if request:
                response.request = request
        else:
            setattr(response, key, value)

    return response

