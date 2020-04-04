import requests

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
	r = requests.get(url)
	return r.elapsed.total_seconds() <= timeout/1000

def check_time_response_post(url, timeout):
	r = requests.post(url)
	return r.elapsed.total_seconds() <= timeout/1000

#response status code 
def check_response_status(url, status):
	r = requests.get(url)
	return r.status_code == status


test_get = check_time_response_get('https://www.google.com', 300)
test_status = check_response_status('https://www.google.com', 300)

print(test_get)
print(test_status)