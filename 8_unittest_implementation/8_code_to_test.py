import requests

def send_request_get(url):
	r = requests.get(url)
	return r

def send_request_post(url, data = None):
	try:
		r = requests.post(url)
		return r
	except Exception as ex:
		return ex

if __name__ ==  '__main__':
	main()