from config_parser import parserConfig
from file_manager_parser import fileManagerAdd


class addItemInterface:
    def __init__(self, wb_id, wm_id, sku):
        self._get_wb_id = wb_id
        self._get_mw_id = wm_id
        self._sku = sku
    #Метод принимает в себя значения для нового товара и возвращает список для записи в бд
    def _get_values_new_item(self):

        return ([f'https://wmart.kz/prod/{self._get_mw_id}/',
                 f'https://www.wildberries.ru/catalog/{self._get_wb_id}/detail.aspx',
                 self._get_wb_id, self._get_mw_id, self._sku])

    #Запускает парсер для добавления нового товара
    def _start_parser_new_item(self, path):
        self._values_wrapper = self._get_values_new_item()

        self._parser = parserConfig(path, self._values_wrapper[0])
        return self._parser.add_item_parse()
    #Метод сохраняет в БД
    def _save_new_item(self, path):
        fm_add = fileManagerAdd(self._start_parser_new_item(path), self._values_wrapper[2], self._values_wrapper[3], self._values_wrapper[0], self._values_wrapper[1], self._values_wrapper[4])
        fm_add.add_item()

    def add_new_item(self, path):
        self._save_new_item(path)


#Функция для экспорта
def add_item(wb_id, wm_id, sku):
    path = 'chromedriver/chromedriver'
    new_item = addItemInterface(wb_id, wm_id, sku)
    new_item.add_new_item(path)
