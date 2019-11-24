#version: v0.0.1
#build-info ^ собрано с локальным тессерактом. дальше перееду на free ocr api , после получения токена
import base64
import re
from selenium import webdriver
from PIL import Image
import requests
from io import BytesIO
import time as tt


class Bot:
	def __init__(self):
		self.browser = webdriver.Chrome()

	def navigate(self,url):
		try: self.browser.get(url)
		except Exception as e: raise e
		# finally: self.browser.quit() 

	def getInfo(self):
		phoneNumber = self.getPhoneNumber()
		price = self.getPrice()
		header = self.getHeader()
		place = self.getPlace()
		info = {"phoneNumber":phoneNumber,
				"price":price,
				"header":header,
				"place":place}
		return info

	def getPhoneNumber(self):
		try:
			buttonNumber = self.browser.find_element_by_css_selector("a[class^=\"button item-phone-button\"][data-side =\"card\"]")
			buttonNumber.click()
			tt.sleep(5)
			imgSource = buttonNumber.find_element_by_tag_name("img").get_attribute("src")
			imgData = bytes(imgSource.split(",")[1], "utf8")
			with open("imageToSave.png", "wb") as fh:
				fh.write(base64.decodebytes(imgData))
		except Exception as ex: raise ex
		finally: return 

	def getPrice(self):
		try:
			priceValue = self.browser.find_element_by_class_name("js-item-price").get_attribute("content")
			priceCurrency = self.browser.find_element_by_css_selector("span[itemprop=\"priceCurrency\"]").get_attribute("content")
			return " ".join([priceValue,priceCurrency])
		except Exception as ex:
			return ex

	def getHeader(self):
		ticketHeader = self.browser.find_element_by_class_name("title-info-title-text").text
		return ticketHeader

	def getPlace(self):
		ticketAddress = self.browser.find_element_by_class_name("item-address__string").text
		return ticketAddress

	def saveResult(self):
		pass

	def dispose(self):
		self.quit()

def main():
	urlList = ["https://www.avito.ru/sankt-peterburg/kvartiry/2-k_kvartira_44.7_m_55_et._1805682679"]
	b = Bot()
	for url in urlList:
		try:
			b.navigate(url)
			info = b.getInfo()
			print(info)
			b.saveResult(info)
		except Exception as ex:
			return ex
			continue
	b.dispose()

if __name__ == "__main__":
	main()