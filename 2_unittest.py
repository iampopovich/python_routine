import requests
import re
import inspect
import unittest

class TestREST(unittest.TestCase):

	def setUp(self):
		self.url = 'https://www.goog0le.com'
		self.timeout = 300
		self.status = 200
		self.text = 'goog0le'

	def check_time_response_get(self):
		r = requests.get(self.url)
		self.assertLessEqual(r.elapsed.total_seconds(), self.timeout/1000 )

	def check_time_response_post(self):
		r = requests.post(self.url)
		self.assertLessEqual(r.elapsed.total_seconds(),self.timeout/1000)

	#response status code 
	def check_response_status(self):
		r = requests.get(self.url)
		self.assertEqual(r.status_code, self.status)

	#response text contains something brrr
	def check_response_contains(self):
		r = requests.get(self.url)
		contains = re.search(self.text,r.text)
		self.assertEqual(bool(contains.group(0), True))

	def runTest(self):
		self.check_response_status()
		self.check_response_contains()
# test_get = check_time_response_get('https://www.goog0le.com', 300)
# test_status = check_response_status('https://www.goo--gle.com', 300)
# test_contains = check_response_contains('https://www.google.com', 'go0gle')

# print(test_get, '\n')
# print(test_status,'\n')
# print(test_contains,'\n')

if __name__ ==  '__main__':
	unittest.TextTestRunner().run(TestREST())