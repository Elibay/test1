import requests

from database import wbDB


class wbApiSender(wbDB):
    def __init__(self):
        super().__init__()


    def post_price_wb(self, wb_id, price):
        headers = {
            'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6IjUxNzdiMGM5LWVkYzAtNDYxZC1hZGUzLThkY2FmMTE4YTEzMiJ9.5qkZz1dpeKrt7EAEKAkej-G512MhBX1UXW2-Xj3Djhs',
            'Content-Type': 'application/json'
        }
        data = []
        data_dict = {'nmId': wb_id, 'price' : price}
        #((float(str(cof[i][0]).replace(",","."))*(int(nm_price[i][0])+700)+(int(nm_price[i][0])+700)))/float((1-float(str(category[i][0]).replace(",", "."))))//get_rate())
        data.append(data_dict)

        res = requests.post(url='https://suppliers-api.wildberries.ru/public/api/v1/prices', headers=headers, json=data)
        print(res.text)


    def post_count_wb(self, sku, count):
        headers = {
            'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6Ijc5NjAzMDZmLTdhYmMtNDM0ZS05M2E3LWVmMmUyOWEyOWZmMCJ9.OJ-0Wcogy-mA4O_SmVfvN_IiCxKx3nGg55KD1zlOUWc',
            'Content-Type': 'application/json'
        }

        warehouse = 647710

        data = []
        data_dict = {"sku": str(sku), 'amount': int(count)}
        data.append(data_dict)
        res = requests.put(f"https://suppliers-api.wildberries.ru/api/v3/stocks/{warehouse}", headers=headers, json={'stocks': data})
        print(res.status_code)


    def send_price(self, wb_id):
        price_wbid = super().add_price_wb(wb_id)
        self.post_price_wb(price_wbid[0], price_wbid[1])


    def send_count(self, wb_id):
        sku_count = super().add_sku_count(wb_id)
        self.post_count_wb(sku_count[0], sku_count[1])
