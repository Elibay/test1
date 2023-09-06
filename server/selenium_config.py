from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#Настройка Selenium
class webBrowser:
    def __init__(self, path):
        self._caps = DesiredCapabilities().CHROME
        self._options = webdriver.ChromeOptions()
        self._options.page_load_strategy = 'eager'
        self._options.add_argument('--headless')
        self._options.add_argument('--no-sandbox')
        self._service = webdriver.ChromeService(executable_path='server/chromedriver/chromedriver')
        self.browser = webdriver.Chrome(service=self._service, options=self._options)
        self.browser.maximize_window()
