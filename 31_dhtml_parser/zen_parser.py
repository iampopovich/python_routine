from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import logging
import time


class Browser(webdriver.Chrome):

    def __init__(self, executable_path):
        super(Browser, self).__init__(executable_path)
        self.logger = logging.getLogger()
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        self.logger.addHandler(sh)

    def get_yandex_zen(self):
        try:
            self.get("https://zen.yandex.ru/")
            time.sleep(5)
        except Exception as ex:
            if self:
                self.quit()
            raise ex

    def scroll_and_parse_zen(self):
        while True:
            self.find_element_by_tag_name("body").send_keys(Keys.END)
            html = self.page_source
            soup = BeautifulSoup(html)
            links = soup.find_all("div", {"class":"card-wrapper__inner"})
            print(len(links))
            time.sleep(1)
            self.logger.info("KEY END PRESSED") #output doesn't appear fuk
        pass


def main():
    try:
        browser = Browser(executable_path="./chromedriver_mac")
        browser.get_yandex_zen()
        browser.scroll_and_parse_zen()
    except Exception as ex:
        if browser:
            browser.quit()
        raise ex
    return None


if __name__ == '__main__':
    main()
