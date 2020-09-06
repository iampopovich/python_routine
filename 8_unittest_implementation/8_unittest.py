import re
import unittest
test = __import__('8_code_to_test')

URL_GET = 'https://www.google.com'
URL_POST = 'http://127.0.0.1'
TIMEOUT_GET = 3000
TIMEOUT_POST = 200
STATUS = 200
TEXT = 'google'


class testResponseStatus(unittest.TestCase):

    def test_response_status(self):
        r = test.send_request_get(URL_GET)
        self.assertEqual(r.status_code, STATUS)


class testResponseoContains(unittest.TestCase):

    def test_response_contains(self):
        r = test.send_request_get(URL_GET)
        contains = re.search(TEXT, r.text)
        self.assertIsNotNone(contains)


class testResponseTime(unittest.TestCase):

    def test_time_response_get(self):
        r = test.send_request_get(URL_GET)
        self.assertLessEqual(r.elapsed.total_seconds(), TIMEOUT_GET/1000)

    def test_time_response_post(self):
        r = test.send_request_post(URL_POST)
        self.assertLessEqual(r.elapsed.total_seconds(), TIMEOUT_POST/1000)


if __name__ == '__main__':
    unittest.main()
