from Browser import Browser

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
