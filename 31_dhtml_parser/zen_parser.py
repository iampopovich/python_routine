from selenium import webdriver
import os
import json
import time
import logging


def init_browser():
    logging.info("инициализирую браузер")
    browser = webdriver.Chrome(executable_path="./chromedriver_mac")
    logging.info("браузер инициализирован")
    return browser


def get_yandex_zen(browser):
    try:
        browser.get("https://zen.yandex.ru/")
        time.sleep(5)
    except Exception as ex:
        if browser:
            browser.quit()
        raise ex


def main():
    browser = None
    try:
        browser = init_browser()
        get_yandex_zen(browser)
    except Exception as ex:
        if browser:
            browser.quit()
        raise ex
    return None


if __name__ == '__main__':
    main()
