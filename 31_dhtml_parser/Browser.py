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
            soup = BeautifulSoup(html, features="html.parser")
            self.search_special_link(soup, 'hernya')
            self.leave_zen_feedback(soup)
            self.check_is_carousel_appears(soup)
            self.logger.info("KEY END PRESSED")  # output doesn't appear fuk
        pass

    def search_special_link(self, soup, link_regex):
        links = soup.find_all("div", {"class": "card-wrapper__inner"})
        print(len(links))
        time.sleep(1)

    def leave_zen_feedback(self, soup):
        feedback = self.find_elements_by_class_name("single-choice-image__item-image")
        if feedback:
            print("FEEDBACK OPTIONS APPEAR AT: {}".format(time.time()))
        # self.leave_zen_good_feedback()

    def check_is_carousel_appears(self, soup):
        carousel = soup.find_all("div", {"class": "personal-carousel-view__carousel"})
        if carousel:
            print("CAROUSEL APPEARS {} AT: {}".format(carousel.__len__(),time.time()))

    def leave_zen_good_feedback(self):
        pass

    def leave_zen_neutral_feedback(self):
        pass

    def leave_zen_bad_feedback(self):
        pass

