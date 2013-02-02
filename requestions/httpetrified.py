# -*- coding: utf-8 -*-
"""
Wraps HTTPretty to make unit testing even better. Instead of specifying the
GET/POST request structure in a unit test, the idea is to save the actual
request using requestions and then load the serialized file for the test.

In the future, this might include some magic to run the test on the live web
for real the first time, then save the data, then load the saved responses the
next time. However, fixturing for multiple requests or multiple responses is
not yet supported.

Usage:

    import json
    import requests
    from requestions import httpetrified

    def get_current_ip_address(self):
        "Abuses some poor sap's ip address detection service."
        response = requests.get("http://jsonip.com")
        return response.json()["ip"]

    @httpetrified("samples/helpers/get-current-ip_address.json")
    def test_get_current_ip_address(self):
        self.assertEqual("127.0.0.1", get_current_ip_address())
"""

import os
import json
import functools

from httpretty import HTTPretty
from httpretty import httprettified

from .io import read_response

def _do_httpretty_registration(path):
    """
    Loads a serialized response through requestions, and sets HTTPretty.
    """
    response = read_response(open(path, "r").read())
    method = getattr(HTTPretty, response.request.method)
    body = response.content
    cookies = response.cookies
    headers = response.headers
    url = response.url
    HTTPretty.register_uri(method, url, body=body, headers=headers, cookies=cookies)

def httpetrified(path):
    """
    A decorator that uses HTTPretty with requestions serialization.
    """
    def _inner(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            HTTPretty.reset()
            HTTPretty.enable()

            _do_httpretty_registration(path)

            try:
                return func(*args, **kwargs)
            finally:
                HTTPretty.disable()
        return wrapper
    return _inner

