import re
import threading
import unittest


class regexTestcase(unittest.TestCase):

	def test_starts_with(self, text, part):
		# result = re.match(r'{}'.format(part), text)
		result = re.search(r'^{}'.format(part), text)
		assertTrue(result)

	def test_ends_with(self,text,part):
		result = re.search(r'{}$'.format(part), text)
		assertTrue(result)

	def test_match_count_less(self, text, part, count):
		result = re.findall(r'{}'.format(part), text)
		assertLess(len(result), count)

	def test_match_count_equal(self, text, part, count):
		result = re.findall(r'{}'.format(part), text)
		assertEqual(len(result), count)

def test_match_count_greater(self, text, part, count):
		result = re.findall(r'{}'.format(part), text)
		assertGreater(len(result), count)

		 
def main():
	return None

if __name__ == '__main__':
	main()