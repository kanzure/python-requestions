# Requestions

Requestions is a serialization library for [Requests](https://github.com/kennethreitz/requests) using JSON.

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

## Changelog

* 0.0.1 - initial commit

## TODO

* hook up with [HTTPretty](https://github.com/gabrielfalcao/HTTPretty) to make unit testing suck less.

## License

BSD.
