from selenium import webdriver
from PIL import Image
import requests
from io import BytesIO

response = requests.get(url)
img = Image.open(BytesIO(response.content))

class Bot:
	def __init__(self):
		self.browser = webdriver.Chrome()

	def navigate(self,url):
		self.browser.get(url)
		self.browser.quit()
		buttonNumber = self.find_element_by_class_name()

def main():
	urlList = []
	b = Bot()
	for url in urlList:
		b.navigate(url)
	pass



if __name__ == "__main__":
	main()