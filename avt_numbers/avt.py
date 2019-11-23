from selenium import webdriver
from PIL import Image
import requests
from io import BytesIO
import time as tt

# response = requests.get(url)
# img = Image.open(BytesIO(response.content))

class Bot:
	def __init__(self):
		self.browser = webdriver.Chrome()

	def navigate(self,url):
		try:
			self.browser.get(url)
			# buttonNumber = self.find_element_by_class_name("")
			buttonNumber = self.browser.find_element_by_css_selector("a[class^=\"button item-phone-button\"][data-side =\"card\"]")
			# button item-phone-button js-item-phone-button button-origin button-origin-blue button-origin_full-width button-origin_large-extra item-phone-button_hide-phone item-phone-button_card js-item-phone-button_card
			buttonNumber.click()
			tt.sleep(5)
			imgSource = buttonNumber.find_element_by_tag_name("img").get_attribute("src")
			# imgSource = self.browser.find_element_by_css_selector("div[class^=\"item-phone-big-number\"] img").get_attribunamete("src")
		except Exception as e: print(e)
		finally : self.browser.quit()

	def loadImage(self, imageSource):
		pass

	def parseImage(self, inputStream):
		pass


def main():
	urlList = ["https://www.avito.ru/sankt-peterburg/kvartiry/2-k_kvartira_44.7_m_55_et._1805682679"]
	b = Bot()
	for url in urlList:
		b.navigate(url)
	pass



if __name__ == "__main__":
	main()