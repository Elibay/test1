from database import wbApiSender
from config_parser import parserConfig
from utils import get_calculation_price, get_rate
from wb_api import send_price_wb



class updateItems(parserConfig):
    def __init__(self, link=None):
        super().__init__(link)
        self.wb_api = wbApiSender()

    def update(self):
        self._items = self.wb_api.send_price('update')
        for i in range(len(self._wm_ids)):
            wm_price = self.update_item_parse(f'https://wmart.kz/prod/{self._items[i][0]}/')
            new_price = get_calculation_price(wm_price, self._items[i][2], self._items[i][3], get_rate())
            send_price_wb(self[i][1], new_price)