import re
from unittest.mock import patch

from homework02 import random_key


def test_random_key():
    test_keys = [f() for f in [random_key]*10]
    assert len(set(test_keys)) == len(test_keys), 'Keys should be different'
    for key in test_keys:
        assert len(key) > 4, 'Key should be at least 5 characters long'
        assert re.match('[\d\w]+', key), 'Key should consist of alphanumeric characters'
 

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200


def test_shorten_redirect_keystats(client):
    test_key = 'dummy'
    test_url = 'http://www.python.org/'

    with patch('homework02.random_key', lambda: test_key):
        response = client.post('/shorten/' + test_url)
        assert response.status_code == 200
        assert test_key in response.content.decode()

        response = client.get('/' + test_key)
        assert response.status_code == 302
        assert response.url == test_url

        response = client.get('/urlstats/' + test_key)
        assert response.status_code == 200
        assert '1' in response.content.decode()


def test_shorten_incorrect_proto(client):
    response = client.post('/shorten/mailto:admin@google.com')
    assert response.status_code == 302
    assert response.url == '/'


def test_redirect_nonexistent(client):
    response = client.get('/randomnonsense')
    assert response.status_code == 302
    assert response.url == '/'
