import pytest

from Browser import Browser


def test_get_zen_page():
    browser = None
    try:
        browser = Browser(executable_path="./chromedriver_mac")
        browser.get_yandex_zen()
        assert browser.page_source == "https://zen.yandex.ru/"
        browser.quit()
    except:
        if browser:
            browser.quit()
