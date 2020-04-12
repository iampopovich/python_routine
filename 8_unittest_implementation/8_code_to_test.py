import requests

def send_request_get(url):
	r = requests.get(url)

def send_request_post(url, data = None):
	r = requests.post(url)

if __name__ ==  '__main__':
	unittest.main()