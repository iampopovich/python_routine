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
		#try:
		self.browser.get(url)
		buttonNumber = self.browser.find_element_by_css_selector("a[class^=\"button item-phone-button\"][data-side =\"card\"]")
		buttonNumber.click()
		tt.sleep(5)
		imgSource = buttonNumber.find_element_by_tag_name("img").get_attribute("src")
		self.browser.quit() #debug stage 
		return imgSource
#		except Exception as e: return e
		# finally : self.browser.quit() #debug stage 

	def saveImage(self, imageSource):
		imgData = bytes(imageSource.split(",")[1], "utf8")
		with open("imageToSave.png", "wb") as fh:
			fh.write(base64.decodebytes(imgData))
		# # with open("image_number.jpg", "wb") as fout:
		# 	fout.write(imgdata)

	def decodeBase64(self,data,altchars=b'+/'):
		data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', bytearray(data, "utf-8"))  # normalize
		missing_padding = len(data) % 4
		if missing_padding:
			data += b'='* (4 - missing_padding)
		return base64.b64decode(data, altchars)

	def parseNumber(self, inputStream):
		pass

	def saveResult(self):
		pass

def main():
	urlList = ["https://www.avito.ru/sankt-peterburg/kvartiry/2-k_kvartira_44.7_m_55_et._1805682679"]
	b = Bot()
	for url in urlList:
		# try:
		imgSource = b.navigate(url)
		b.saveImage(imgSource)
			# phoneNumber = b.parseNumber(localImage)
			# b.saveResult()
		# except Exception as ex:
		# 	return ex
		# 	continue
	return None

if __name__ == "__main__":
	main()