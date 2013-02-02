# -*- coding: utf-8 -*-

import json
import unittest
import requests

import requestions

from requestions import httpetrified

class TestRequestSerialization(unittest.TestCase):
    def test_write_request_simple(self):
        request = requests.models.Request(url="http://httpbin.org/get")
        srequest = requestions.write_request(request, return_string=False)
        self.assertIn("method", srequest.keys())
        self.assertIn("headers", srequest.keys())
        self.assertIn("params", srequest.keys())
        self.assertIn("url", srequest.keys())

    def test_write_request_strings(self):
        request = requests.models.Request(url="http://httpbin.org/get")
        srequest = requestions.write_request(request)
        parsed = json.loads(srequest)
        self.assertIn("method", parsed.keys())
        self.assertIn("headers", parsed.keys())

    def test_write_request_headers(self):
        given_headers = {"test_header": "test_value"}
        request = requests.models.Request(url="http://httpbin.org/get", headers=given_headers)
        srequest = requestions.write_request(request, return_string=False)
        self.assertIn("headers", srequest.keys())
        self.assertEqual(given_headers, srequest["headers"])

    def test_write_request_url(self):
        given_url = "http://httpbin.org/get"
        request = requests.models.Request(url=given_url)
        srequest = requestions.write_request(request, return_string=False)
        self.assertIn("url", srequest.keys())
        self.assertEqual(given_url, srequest["url"])

class TestRequestDeserialization(unittest.TestCase):
    def test_read_request_url(self):
        given_url = "http://httpbin.org/get"
        srequest = json.dumps({"url": given_url})
        request = requestions.read_request(srequest)
        self.assertEqual(given_url, request.url)

class TestResponseSerialization(unittest.TestCase):
    def test_write_response_simple(self):
        given_url = "http://httpbin.org/get"
        response = requests.models.Response()
        response.url = given_url
        sresponse = requestions.write_response(response, return_string=False)
        self.assertIn("url", sresponse.keys())
        self.assertEqual(given_url, sresponse["url"])

class TestResponseDeserialization(unittest.TestCase):
    def test_read_response_simple(self):
        given_url = "http://httpbin.org/get"
        sresponse = json.dumps({"url": given_url})
        response = requestions.read_response(sresponse)
        self.assertEqual(given_url, response.url)

class TestSerialization(unittest.TestCase):
    def test_requests_pedantically(self):
        given_url = "http://httpbin.org/get"
        given_method = "GET"
        given_headers = {"User-Agent": "Charmander/1.0"}
        given_cookies = {"__utm_soul_tracking_id": "A941ECF10959101"}
        given_request = requests.models.Request(url=given_url, method=given_method, headers=given_headers, cookies=given_cookies)
        given_srequest = requestions.write_request(given_request)
        request = requestions.read_request(given_srequest)
        self.assertEqual(request.url, given_request.url)
        self.assertEqual(request.headers, given_headers)
        self.assertEqual(request.method, given_method)
        self.assertEqual(dict(request.cookies), given_cookies)

    def test_responses_pedantically(self):
        given_url = "http://httpbin.org/get"
        given_headers = {"User-Agent": "Charmander/1.0"}
        given_cookies = {"__utm_soul_tracking_id": "A941ECF10959101"}
        given_status_code = 200
        given_content = "foo123"
        given_response = requests.models.Response()
        given_response.url = given_url
        given_response.headers = given_headers
        given_response.cookies = given_cookies
        given_response.status_code = given_status_code
        given_response._content = given_content
        given_sresponse = requestions.write_response(given_response)
        response = requestions.read_response(given_sresponse)
        self.assertEqual(response.url, given_response.url)
        self.assertEqual(response.headers, given_headers)
        self.assertEqual(response.status_code, given_status_code)
        self.assertEqual(dict(response.cookies), given_cookies)
        self.assertEqual(response.content, given_content)

class TestUtilities(unittest.TestCase):
    def test_replace_body_with_data(self):
        stuff = "mestanolone"
        sample = {"body": stuff}
        requestions.utils.replace_body_with_data(sample)
        self.assertNotIn("body", sample.keys())
        self.assertIn("data", sample.keys())

    def test_delete_blank_keys_from(self):
        blank_keys = ["one", "two", "three", "four"]
        sample = {"body": "stuff",}
        sample.update(dict([(key, None) for key in blank_keys]))
        requestions.utils.delete_blank_keys_from(sample)
        self.assertIn("body", sample.keys())
        for key in blank_keys:
            self.assertNotIn(key, sample.keys())

    def test_get_and_del_attr(self):
        sample = {
            "key0": "value0",
            "key1": "value1",
        }
        value0 = requestions.utils.get_and_del_attr(sample, "key0")
        self.assertEqual(value0, "value0")
        self.assertNotIn("key0", sample.keys())
        value1 = requestions.utils.get_and_del_attr(sample, "key1")
        self.assertEqual(value1, "value1")
        self.assertNotIn("key1", sample.keys())
        self.assertEqual(0, len(sample.keys()))

class TestHttpetrifiedDecorator(unittest.TestCase):
    @httpetrified("tests/data/jsonip-response.json")
    def test_basic_decorator(self):
        response = requests.get("http://jsonip.com/")
        try:
            jsonstuff = resposne.json()
        except Exception as exception:
            jsonstuff = response.json
        self.assertEqual(jsonstuff["ip"], "66.68.190.37")

if __name__ == "__main__":
    unittest.main()
