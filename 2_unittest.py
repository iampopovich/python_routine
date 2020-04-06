import requests
import re
import inspect
import unittest

URL = 'https://www.google.com'
TIMEOUT = 300
STATUS = 200
TEXT = 'google'

class testResponseStatus(unittest.TestCase): #remember pep-8 and refactor it !

	def setUp(self):
		self.url = URL
		self.timeout = TIMEOUT
		self.status = STATUS
		self.text = TEXT

	def test_response_status(self):
		r = requests.get(self.url)
		self.assertEqual(r.status_code, self.status)

	def test_response_contains(self):
		r = requests.get(self.url)
		contains = re.search(self.text,r.text)
		self.assertIsNotNone(contains)

class testResponseTime(unittest.TestCase):
# Remember DRY and refactore it !

	def setUp(self):
		self.url = URL
		self.timeout = TIMEOUT
		self.status = STATUS
		self.text = TEXT


	def test_time_response_get(self):
		r = requests.get(self.url)
		self.assertLessEqual(r.elapsed.total_seconds(), self.timeout/1000 )

	def test_time_response_post(self):
		r = requests.post(self.url)
		self.assertLessEqual(r.elapsed.total_seconds(),self.timeout/1000)

if __name__ ==  '__main__':
	unittest.main()