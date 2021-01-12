import unittest
from Browser import Browser


class BrowserBaseTest(unittest.TestCase):

    def test_get_zen_page(self):
        browser = None
        try:
            browser = Browser(executable_path="./chromedriver_mac")
            browser.get_yandex_zen()
            self.assertEqual(browser.page_source, "https://zen.yandex.ru/")
            browser.quit()
        except:
            if browser:
                browser.quit()


if __name__ == '__main__':
    unittest.main()
