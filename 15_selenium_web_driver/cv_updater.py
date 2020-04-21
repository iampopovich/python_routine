from selenium import webdriver
import json
import time

def get_config():
	with open('cred.cfg', 'r') as c:
		config = json.load(c)
	return config

def init_browser(path):
	browser = webdriver.Chrome(executable_path = path)
	return browser

def autorize(browser, config):
	try:
		browser.get('https://spb.hh.ru/account/login?backurl=%2F')
		time.sleep(5)
		form_login = browser.find_element_by_xpath('//input[@data-qa="login-input-username"]')
		form_password = browser.find_element_by_xpath('//input[@data-qa="login-input-password"]')
		form_login.send_keys(config['login'])
		form_password.send_keys(config["password"])
		button_submit = browser.find_element_by_xpath('//input[@data-qa="account-login-submit"]')
		button_submit.click()
		return browser
	except:
		browser.exit()

def update_cv(browser,url):
	browser.get(url)
	time.sleep(10)
# <button class="bloko-button bloko-button_primary bloko-button_stretched" type="button" disabled="" data-qa="resume-update-button">Обновить дату </button>

	return None

def main():
	while True:
		try:
			config = get_config()
			browser = init_browser(config['browserPath'])
			browser = autorize(browser,config)
			update_cv(browser, config['resumeID'])
			browser.close()
			time.sleep(20)
		except:
			browser.close()
	return None

if __name__ == '__main__':
	main()