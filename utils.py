from selenium import webdriver


def create_chrome_driver(*, headless=False):
    """创建 chrome webdriver"""
    option = webdriver.ChromeOptions()
    if headless:
        option.add_argument('--headless')
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(options=option)
    browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                            {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined'}
                            )
    return browser
