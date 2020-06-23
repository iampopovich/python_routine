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
		form_login = browser.find_element_by_xpath(
			'//input[@data-qa="login-input-username"]'
			)
		form_password = browser.find_element_by_xpath(
			'//input[@data-qa="login-input-password"]'
			)
		form_login.send_keys(config['login'])
		form_password.send_keys(config["password"])
		button_submit = browser.find_element_by_xpath(
			'//input[@data-qa="account-login-submit"]'
			)
		button_submit.click()
		return browser
	except Exception as ex:
		browser.quit()
		raise ex

def send_reply(browser, config):
	try:
		resume_id = config['resumeID']
		reply_text = config['replyMessage']
		replies = config['reply']
		browser.get('https://spb.hh.ru/search/vacancy?order_by=publication_time&clusters=true&resume={}&enable_snippets=true'.format(resume_id))
		time.sleep(10)
		list_vacancy = browser.find_elements_by_class_name('vacancy-serp-item')
		replied = 0
		for v in list_vacancy:
			try:
				if replied == replies: break
				reply_vacancy = v.find_element_by_xpath(
					'.//a[@data-qa="vacancy-serp__vacancy_response"]'
					)
				browser.execute_script("arguments[0].click();", reply_vacancy)
				time.sleep(5)
				reply_message = browser.find_element_by_xpath(
					'/html/body/div[9]/div[1]/div/form/div[2]/div[2]/span/span'
					) #факап
				reply_message.click()
				reply_message_text = browser.find_element_by_xpath(
					'/html/body/div[9]/div[1]/div/form/div[2]/div[2]/div/textarea'
					) #факап
				reply_message_text.send_keys(reply_text)
				button_submit = browser.find_element_by_xpath(
					'/html/body/div[9]/div[1]/div/form/div[4]/div/button'
					) #факап
				button_submit.click()
				time.sleep(5)
				replied+=1
			except Exceptions as ex:
				# raise ex
				continue #глушу пока
	except Exception as ex:
		browser.quit()
		raise ex

def add_favorite(browser,resume_id):
	return None

def update_cv(browser,resume_id):
	try:
		browser.get('https://spb.hh.ru/resume/{}'.format(resume_id))
		time.sleep(10)
		button_submit = browser.find_element_by_xpath(
			'//button[@data-qa="resume-update-button"]'
			)
		if button_submit.is_enabled():
			browser.execute_script("arguments[0].click();", button_submit)
		# actions = ActionChains(browser)
		# actions.move_to_element(button_submit).perform()
		# button_submit.click()
	except Exception as ex:
		raise ex

def main():
	while True:
		try:
			config = get_config()
			browser = init_browser(config['browserPath'])
			browser = autorize(browser, config)
			update_cv(browser, config['resumeID'])
			if config['reply'] != 0: pass #send_reply(browser, config) #unstable fusnctionality will be tested and deployed in next version 
			browser.quit()
			time.sleep(14450) #ласно правилам ХХ можно апдейтить CV  раз в 4 часа
		except Exception as ex:
			browser.quit()
			raise ex
	return None

if __name__ == '__main__':
	main()