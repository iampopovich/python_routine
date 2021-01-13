import unittest

from Browser import Browser


class BrowserBaseTest_unittest(unittest.TestCase):

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

    def test_response_status_is_200(self):
        browser = None
        try:
            browser = Browser(executable_path="./chromedriver_mac")
            browser.get_yandex_zen()
            for request in browser.requests:
                if request.response.url == "https://zen.yandex.ru/":
                    print(request.response)
                    self.assertEqual(request.response.status_code, 200)
        except:
            if browser:
                browser.quit()


if __name__ == '__main__':
    unittest.main()
