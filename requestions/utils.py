# -*- coding: utf-8 -*-
"""
Minor functions to assist with (de)serializing.
"""

# for dealing with requests.models.Response.request.body
try:
    import urlparse
except ImportError: # py3k
    import urllib.parse as urlparse

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
    Deletes from the given dictionary any key/value pair where the value
    evaluates to False, including False, '', {}, [], and (,).
    """
    for key in list(some_dict.keys()):
        if not some_dict[key]:
            del some_dict[key]

