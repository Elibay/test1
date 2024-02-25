import requests


def get_rate():
    return round(100 / requests.get(url='https://www.cbr-xml-daily.ru/daily_json.js') \
                 .json()['Valute']['KZT']['Value'], 1)


def get_calculation_price(price, category, cof, ff_and_logistic, rate):
    print(price, '-----------------------------')
    valid_price = int(str(price).replace(" ", '').strip())
    price_minus_10_percent = int(valid_price) - (int(valid_price) / 100) * 10
    print(rate)
    return int(
        (float(cof.replace(',', '.')) * (int(price_minus_10_percent) + ff_and_logistic) + (
                    int(price_minus_10_percent) + ff_and_logistic)) / (
                1 - float(category.replace(",", '.'))) / rate)
