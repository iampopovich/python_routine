import requests
import re
import inspect


def check_time_response_get(url, timeout):
    try:
        r = requests.get(url)
        return r.elapsed.total_seconds() <= timeout/1000
    except Exception as ex:
        return 'Error in {}: {}'.format(inspect.stack()[0][3], ex)


def check_time_response_post(url, timeout):
    r = requests.post(url)
    return r.elapsed.total_seconds() <= timeout/1000


def check_response_status(url, status):
    try:
        r = requests.get(url)
        return r.status_code == status
    except Exception as ex:
        return 'Error in {}: {}'.format(inspect.stack()[0][3], ex)


def check_response_contains(url, text):
    try:
        r = requests.get(url)
        contains = re.search(text, r.text)
        return bool(contains.group(0))
    except Exception as ex:
        return 'Error in {}: {}'.format(inspect.stack()[0][3], ex)


test_get = check_time_response_get('https://www.goog0le.com', 300)
test_status = check_response_status('https://www.goo--gle.com', 300)
test_contains = check_response_contains('https://www.google.com', 'go0gle')


print(test_get, '\n')
print(test_status, '\n')
print(test_contains, '\n')
