import requests
import re
import inspect
import unittest

class testResponseStatus(unittest.TestCase): #remember pep-8 and refactor it !

	def setUp(self):
		self.url = 'https://www.google.com'
		self.timeout = 300
		self.status = 2000
		self.text = 'google'

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
		self.url = 'https://www.google.com'
		self.timeout = 300
		self.status = 200
		self.text = 'google'

	def test_time_response_get(self):
		r = requests.get(self.url)
		self.assertLessEqual(r.elapsed.total_seconds(), self.timeout/1000 )

	def test_time_response_post(self):
		r = requests.post(self.url)
		self.assertLessEqual(r.elapsed.total_seconds(),self.timeout/1000)

if __name__ ==  '__main__':
	unittest.main()