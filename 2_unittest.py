import requests
import re
import inspect
import unittest

URL_GET = 'https://www.google.com'
URL_POST = ''
TIMEOUT_GET = 300
TIMEOUT_POST = 200
STATUS = 200
TEXT = 'google'


class testResponseStatus(unittest.TestCase):

    def test_response_status(self):
        r = requests.get(URL_GET)
        self.assertEqual(r.status_code, STATUS)


class testResponseoContains(unittest.TestCase):

    def test_response_contains(self):
        r = requests.get(URL_GET)
        contains = re.search(TEXT, r.text)
        self.assertIsNotNone(contains)


class testResponseTime(unittest.TestCase):

    def setUp(self):
        self.url_get = URL_GET
        self.url_post = URL_POST
        self.timeout_get = TIMEOUT_GET
        self.timeoit_post = TIMEOUT_POST
        self.status = STATUS
        self.text = TEXT

    def test_time_response_get(self):
        r = requests.get(self.url_get)
        self.assertLessEqual(r.elapsed.total_seconds(), self.timeout_get/1000)

    def test_time_response_post(self):
        r = requests.post(self.url_post)
        self.assertLessEqual(r.elapsed.total_seconds(), self.timeout_post/1000)


if __name__ == '__main__':
    unittest.main()
