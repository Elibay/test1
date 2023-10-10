import requests

from database import wbDB


class wbApiSender(wbDB):
    def __init__(self):
        super().__init__()


    def post_price_wb(wb_id, price):
        headers = {
            'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6Ijc5NjAzMDZmLTdhYmMtNDM0ZS05M2E3LWVmMmUyOWEyOWZmMCJ9.OJ-0Wcogy-mA4O_SmVfvN_IiCxKx3nGg55KD1zlOUWc',
            'Content-Type': 'application/json'
        }
        data = []
        data_dict = {'nmId': wb_id, 'price' : price}
        #((float(str(cof[i][0]).replace(",","."))*(int(nm_price[i][0])+700)+(int(nm_price[i][0])+700)))/float((1-float(str(category[i][0]).replace(",", "."))))//get_rate())
        data.append(data_dict)

        res = requests.post(url='https://suppliers-api.wildberries.ru/public/api/v1/prices', headers=headers, json=data)
        print(res.text)


    def send_price(self, action, wb_id):
        price_wbid = super().get_price_wb(action=action, wb_id=wb_id)
        print(price_wbid)
        self.post_price_wb(wb_id=price_wbid[0], price=price_wbid[1])


    def send_count(self, sku, count):
        pass