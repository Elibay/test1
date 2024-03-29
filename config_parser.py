from selenium_config import webBrowser
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time

class parserConfig:
    def __init__(self, link = None):
        self._browser = webBrowser().browser
        self._link = link

    #Возвращает Selenium объект, в котором содержиться обертка с ценами
    def _get_price_wrapper(self):
        __get_offers_wrapper = self._browser.find_element(By.CLASS_NAME, 'offers_price_wrapper')
        return __get_offers_wrapper.find_elements(By.TAG_NAME, 'div')

    #Возвращает стороку, Имя товара
    def _get_name(self):
        return self._browser.find_element(By.ID, 'pagetitle').text

    #Возвращает кортеж из цен: текущая цена со скидкой, цена до скидки
    def _get_price(self):
        _wrapper = self._get_price_wrapper()
        print(len(_wrapper))
        time.sleep(5)
        if len(_wrapper) < 2:
            _current_price = 0
            _old_price = _wrapper[0].find_element(By.CLASS_NAME, 'price_value').text
            print(_old_price)
            time.sleep(5)
        else:
            _current_price = str(_wrapper[0].find_element(By.CLASS_NAME, 'price_value').text).replace(' ', '')
            _old_price = _wrapper[1].find_element(By.CLASS_NAME, 'price_value').text
        return (_current_price, _old_price)


    #Возвращает число: общее количество со всех складов
    def _get_item_count(self):
        count = 0
        _get_element_count_wrapper = self._browser.find_element(By.CLASS_NAME, 'list-amount').find_elements(By.TAG_NAME, 'li')
        for i in range(len(_get_element_count_wrapper[1:3])):
            tmp = _get_element_count_wrapper[1:3][i].find_element(By.CLASS_NAME, 'count').text
            if tmp[:-4].isdigit():
                count += int(tmp[:-4])
        return count

    #Запускает парсер и возвращает список значений для добавления нового товара
    def add_item_parse(self):
        self._browser.get(self._link)
        self._proxy_element = self._browser.find_element(By.TAG_NAME, 'body')
        try:
            self._prices = self._get_price()
            self._count = self._get_item_count()
            self._proxy_element.send_keys(Keys.ESCAPE)
            self._list_values =  [self._get_name(), self._prices[1], self._count]
            self._browser.close()
            return self._list_values
        except Exception:
            return [None,None,None,None]

    #Запускает парсер и возвращает обновленые цены
    def update_item_parse(self, wm_links):
        self._browser.get(wm_links)
        time.sleep(3)
        self._new_current_price = self._get_price()[1]
        self._new_count = self._get_item_count()
        return self._new_current_price, self._new_count
