from database import wbDB, updateItemsDb
from config_parser import parserConfig
from utils import get_calculation_price, get_rate
from wb_api import wbApiSender



class updateItems(parserConfig):
    def __init__(self, link=None):
        super().__init__(link)
        self.wb_db = wbDB()
        self.wbApi = wbApiSender()
        self.upd = updateItemsDb()

    def update(self):
        self._items = self.wb_db.update_items()
        for i in range(len(self._items)):
            wm = self.update_item_parse(f'https://wmart.kz/prod/{self._items[i][0]}/')
            new_price = get_calculation_price(wm[0], self._items[i][2], self._items[i][3], get_rate())
            self.upd.update_item(new_price, wm[1], self._items[i][1])
            self.wbApi.send_price(self._items[i][1])
            self.wbApi.send_count(self._items[i][1])
        self.upd.con.close()

upd = updateItems()
upd.update()
