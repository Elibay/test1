import requests

def get_rate():
    return round(100 / requests.get(url='https://www.cbr-xml-daily.ru/daily_json.js')\
                   .json()['Valute']['KZT']['Value'], 1)
#Отправляет цены
def post_price(nm_price, cof):
    print(cof[0][0])
    headers = {
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6Ijc5NjAzMDZmLTdhYmMtNDM0ZS05M2E3LWVmMmUyOWEyOWZmMCJ9.OJ-0Wcogy-mA4O_SmVfvN_IiCxKx3nGg55KD1zlOUWc',
        'Content-Type': 'application/json'
    }
    data = []
    for i in range(len(nm_price)):
        if nm_price[i][0] != None:
            data_dict = {'nmId': int(str(nm_price[i][1]).replace(".", "")), 'price' : ((int(nm_price[i][0])+550+575)*float(str(cof[i][0]).replace(",",".")))//get_rate()}
            data.append(data_dict)

    res = requests.post(url='https://suppliers-api.wildberries.ru/public/api/v1/prices', headers=headers, json=data)
    print(res.text)
#Отправляет остатки
def post_amount(sku_count):

    warehouse = 647710
    headers = {
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NJRCI6Ijc5NjAzMDZmLTdhYmMtNDM0ZS05M2E3LWVmMmUyOWEyOWZmMCJ9.OJ-0Wcogy-mA4O_SmVfvN_IiCxKx3nGg55KD1zlOUWc',
        'Content-Type': 'application/json'
    }

    data = []
    for i in range(len(sku_count)):
        data_dict = {'sku':f'{sku_count[i][1]}', 'amount': sku_count[i][0]}
        data.append(data_dict)


    res = requests.put(url=f'https://suppliers-api.wildberries.ru/api/v3/stocks/{warehouse}', headers=headers, json={'stocks':data})
    print(res.text)
