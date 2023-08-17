from config_parser import parserConfig
from file_manager_parser import fileManagerUpdate
from wb_api import post_amount, post_price

class updateItemsInterface:
    #Обновляет значения в БД
    def update_price(self,path):
        self._fm = fileManagerUpdate()
        self._parser = parserConfig(path)
        self._fm.update_price_records(self._parser.update_item_parse(self._fm.get_links_for_update()))


def update_item():
    path = 'chromedriver/chromedriver.exe'
    upi = updateItemsInterface()
    upi.update_price(path)

def main():
    update_item()

if __name__=='__main__':
    main()
