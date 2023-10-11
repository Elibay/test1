from flask import Flask, render_template, request, redirect

from database import addNewItem, getItems, delItem
from wb_api import wbApiSender

app = Flask(__name__)



add = {'name': 'добавить', 'url': '/add'}


@app.route('/', methods=['POST', 'GET'])
def index():
    items = getItems()
    items = items.get_items()

    if request.method == 'POST':
        di = delItem()
        di.del_item(request.form['wm_id'])
        return redirect('/')
    return render_template('index.html', items = items, len = len(items['name']), add = add)


@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        new_item = addNewItem(request.form['wm_id'], request.form['wb_id'], request.form['sku'], request.form['cof'], request.form['category'])
        new_item.add_item()
        wb = wbApiSender()
        wb.send_price(request.form['wb_id'])
        wb.send_count(request.form['wb_id'])
        return redirect('/')
    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)