import requests
import re
import inspect

# #create a request object 
# r_get = requests.get('https://www.google.com')
# r_put = requests.put('http://httpbin.org/put')
# r_del = requests.delete('http://httpbin.org/delete')
# r_head = requests.head('http://httpbin.org/get') #https://developer.mozilla.org/ru/docs/Web/HTTP/Methods/HEAD
# r_opt = requests.options('http://httpbin.org/get') #https://developer.mozilla.org/ru/docs/Web/HTTP/Methods/OPTIONS

# #let see what's inside
# print(r_get.status_code)
# print(r_get.content[:100])
# # print('\n'.join(r_get.cookies.split(',')))
# print(r_get.cookies.items(),'\n')
# print(r_get.cookies.get_dict(),'\n')

#response time measurement 
def check_time_response_get(url, timeout):
	try:
		r = requests.get(url)
		return r.elapsed.total_seconds() <= timeout/1000
	except Exception as ex:
		return 'Error in {}: {}'.format(inspect.stack()[0][3], ex)


def check_time_response_post(url, timeout):
	r = requests.post(url)
	return r.elapsed.total_seconds() <= timeout/1000

#response status code 
def check_response_status(url, status):
	try:
		r = requests.get(url)
		return r.status_code == status
	except Exception as ex:
		return 'Error in {}: {}'.format(inspect.stack()[0][3], ex)

#response text contains something brrr
def check_response_contains(url, text):
	try:
		r = requests.get(url)
		contains = re.search(text,r.text)
		return bool(contains.group(0))
	except Exception as ex:
		return 'Error in {}: {}'.format(inspect.stack()[0][3], ex)

test_get = check_time_response_get('https://www.goog0le.com', 300)
test_status = check_response_status('https://www.goo--gle.com', 300)
test_contains = check_response_contains('https://www.google.com', 'go0gle')


print(test_get, '\n')
print(test_status,'\n')
print(test_contains,'\n')