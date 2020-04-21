from selenium import webdriver
import json
import time
import logging

def get_config():
	logging.info("получаю конфигурацию приложения")
	with open('cred.cfg', 'r') as c:
		config = json.load(c)
	logging.info("конфигурация получена")
	return config

def init_browser(path):
	logging.info("инициализирую браузер")
	browser = webdriver.Chrome(executable_path = path)
	logging.info("браузер инициализирован")
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
	except Exception as ex:
		browser.exit()
		raise ex

def send_reply(browser, config):
	try:
		resume_id = config['resumeID']
		reply_text = config['replyMessage']
		replies = config['reply']
		browser.get('https://spb.hh.ru/search/vacancy?order_by=publication_time&clusters=true&resume=f{}&enable_snippets=true'.format(resume_id))
		time.sleep(10)
		list_vacancy = browser.find_elements_by_class_name('vacancy-serp-item')
		replied = 0
		for v in list_vacancy:
			if browser.find_element_by_xpath('//a[@data-qa="vacancy-serp__vacancy_response"]'):
				if replied == replies: break
				reply_vacancy = browser.find_element_by_xpath('//a[@data-qa="vacancy-serp__vacancy_response"]')
				reply_vacancy.click()
				reply_message = browser.find_element_by_xpath('//span[@data-qa="vacancy-response-letter-toggle"]')
				reply_message.click()
				reply_message_text = browser.find_element_by_name('letter')
				reply_message_text.send_keys(reply_text)
				button_submit = browser.find_element_by_xpath('//button[@data-qa="vacancy-response-submit-popup"]')
				button.click()
				time.sleep(5)
				replied+=1
			if browser.find_element_by_xpath('//a[@data-qa="vacancy-serp__vacancy_responded"]'): continue
	except Exception as ex:
		browser.exit()
		raise ex

def add_favorite(browser,resume_id):
	return None

def update_cv(browser,resume_id):
	try:
		browser.get('https://spb.hh.ru/resume/{}'.format(resume_id))
		time.sleep(10)
		button_submit = browser.find_element_by_xpath('//input[@data-qa="resume-update-button"]')
		button_submit.click()
	except Exception as ex:
		raise ex

def main():
	while True:
		try:
			config = get_config()
			browser = init_browser(config['browserPath'])
			browser = autorize(browser, config)
			update_cv(browser, config['resumeID'])
			if int(config['reply']) != 0: send_reply(browser, config)
			browser.close()
			time.sleep(14450) #ласно правилам ХХ можно апдейтить CV  раз в 4 часа
		except Exception as ex:
			browser.close()
			raise ex
	return None

if __name__ == '__main__':
	main()