# -*- coding: utf-8 -*-
"""
Minor functions to assist with (de)serializing.
"""

# for dealing with requests.models.Response.request.body
import urlparse

def replace_body_with_data(things):
    """
    Modifies a dictionary to replace 'body' with 'data' for deserialization
    later.
    """
    if "body" in things.keys() and things["body"] != None:
        data = urlparse.parse_qs(things["body"])
        things["data"] = data
        del things["body"]

def delete_blank_keys_from(some_dict):
    """
    Deletes keys that have None values in the given dictionary.
    """
    for key in some_dict.keys():
        if not some_dict[key]:
            del some_dict[key]

def get_and_del_attr(some_dict, key):
    """
    Gets the value for some key, then removes the key from the dictionary.
    Returns the value.
    """
    value = None
    if key in some_dict.keys():
        value = some_dict[key]
        del some_dict[key]
    return value
