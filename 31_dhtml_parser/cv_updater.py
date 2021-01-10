from selenium import webdriver
import os
import json
import time
import logging


class Browser(webdriver.Chrome)

   def __init__(self):
        logging.info("инициализирую браузер")
        browser = webdriver.Chrome(executable_path="./chromedriver_mac")
        logging.info("браузер инициализирован")
        return browser

    def get_yandex_zen(self):
        try:
            self.get("https://zen.yandex.ru/")
            time.sleep(5)
        except Exception as ex:
            if self:
                self.quit()
            raise ex


    def scroll_and_parse_zen(self):
        pass


def main():
    try:
        browser = Browser()
        browser.get_yandex_zen()
        browser.scroll_and_parse_zen()
    except Exception as ex:
        if browser:
            browser.quit()
        raise ex
    return None


if __name__ == '__main__':
    main()
