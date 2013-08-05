# Requestions

Requestions is a serialization library for [Requests](https://github.com/kennethreitz/requests) using JSON. Also, requestions includes a decorator called httpetrified for storing responses and replaying them in the future for HTTP testing without the live interwebz.

## Installing

Simple.

``` bash
sudo pip install requestions
```

or,

``` bash
sudo python setup.py install
```

## Usage

``` python
# responses
original_response = requests.get("http://httpbin.org/get")
serialized_response = requestions.write_response(original_response)
response = requestions.read_response(serialized_response)

# requests
original_request = requests.models.Request(url="http://httpbin.org/post", method="POST")
serialized_request = requestions.write_request(original_request)
request = requestions.read_request(serialized_request)
```

## Decorator

Save responses in a json file, then use them later to make unit testing not so miserable.

``` python
import json
import requests
from requestions import httpetrified

def get_current_ip_address(self):
    "Abuses some poor sap's ip address detection service."
    response = requests.get("http://jsonip.com")
    return response.json()["ip"]

@httpetrified("samples/helpers/jsonip-request.json")
def test_get_current_ip_address(self):
    self.assertEqual("127.0.0.1", get_current_ip_address())
```

## Changelog

* 0.0.7 - fix CaseInsensitiveDict problem
* 0.0.5 - fix broken setup.py, gah
* 0.0.4 - fix test for both requests==0.14.2 and requests>=1.0.3
* 0.0.3 - httpetrified decorator
* 0.0.1 - initial commit

## Alternatives

* [requests-vcr](https://github.com/sigmavirus24/requests-vcr)

## Related

* [HTTPretty](https://github.com/gabrielfalcao/HTTPretty)

## TODO

* support multiple requests/responses in a single json file. This will allow a
  single test to cause multiple requests to be made that can all be mocked
  simultaneously.

* support streaming http responses like HTTPretty does

## License

BSD.
