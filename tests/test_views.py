import pytest
import urllib


def test_api_parse_succeeds(client):
    address_string = '123 main st chicago il'
    url = encode_address_for_query_string(address_string)
    response = client.get(url)
    
    assert response.status_code == 200
    assert response.data.get('input_string') == address_string
    assert response.data.get('address_type') == 'Street Address'
    assert isinstance(response.data.get('address_components'), dict)


def test_api_parse_raises_error(client):
    address_string = '123 main st chicago il 123 main st'
    url = encode_address_for_query_string(address_string)
    response = client.get(url)
    assert response.status_code == 400

    empty_string = ''
    url = encode_address_for_query_string(empty_string)
    response = client.get(url)
    assert response.status_code == 400


def encode_address_for_query_string(address_string):
    query_string = urllib.parse.urlencode({'address': address_string})
    url = f'/api/parse/?{query_string}'
    return url