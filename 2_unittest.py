import requests
import re
import inspect
import unittest

class TestREST(unittest.TestCase):

	def setUp(self):
		self.url = 'https://www.google.com'
		self.timeout = 300
		self.status = 2000
		self.text = 'go00ogle'

	def test_time_response_get(self):
		r = requests.get(self.url)
		self.assertLessEqual(r.elapsed.total_seconds(), self.timeout/1000 )

	def test_time_response_post(self):
		r = requests.post(self.url)
		self.assertLessEqual(r.elapsed.total_seconds(),self.timeout/1000)

	def test_response_status(self):
		r = requests.get(self.url)
		self.assertEqual(r.status_code, self.status)

	def test_response_contains(self):
		r = requests.get(self.url)
		contains = re.search(self.text,r.text)
		self.assertIsNotNone(contains)

	# def runTest(self):
	# 	self.check_response_status()
	# 	self.check_response_contains()


# test_get = check_time_response_get('https://www.goog0le.com', 300)
# test_status = check_response_status('https://www.goo--gle.com', 300)
# test_contains = check_response_contains('https://www.google.com', 'go0gle')

# print(test_get, '\n')
# print(test_status,'\n')
# print(test_contains,'\n')

if __name__ ==  '__main__':
	# unittest.TextTestRunner().run(TestREST())
	unittest.main()