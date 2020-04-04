import requests

#create a request object 
r_get = requests.get('https://www.google.com')
r_put = requests.put('http://httpbin.org/put')
r_del = requests.delete('http://httpbin.org/delete')
r_head = requests.head('http://httpbin.org/get') #https://developer.mozilla.org/ru/docs/Web/HTTP/Methods/HEAD
r_opt = requests.options('http://httpbin.org/get') #https://developer.mozilla.org/ru/docs/Web/HTTP/Methods/OPTIONS
