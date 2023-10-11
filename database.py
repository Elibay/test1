import sqlite3
from config_parser import parserConfig
from utils import get_rate, get_calculation_price


class database:
    """ Класс для создания и подключения к базе данных """
    def __init__(self):
        self.con = sqlite3.connect('WM_WB.db', check_same_thread=False)
        self.cur = self.con.cursor()
        self.cur.execute('CREATE TABLE if not exists wb_wm(id INTEGER PRIMARY KEY AUTOINCREMENT,\
                    name STRING, current_price INTEGER, old_price INTEGER, count INTEGER, wb_id INTEGER,\
                     wm_id INTEGER, wb_link STRING, wm_link STRING, sku STRING, cof REAL, category REAL)')


class getItems(database):
    """ Класс для получения товаров из базы данных """
    def __init__(self):
        super().__init__()

    """ Метод возварщает словарь формата {'key': (items, ..., n)} """
    def get_items(self):
        items = self.cur.execute('SELECT name, current_price, old_price, count, wb_id, wm_id, wb_link, wm_link, sku, cof, category FROM wb_wm').fetchall()
        items_dict = {
            'name' : tuple(i[0] for i in items),
            'current_price': tuple(i[1] for i in items),
            'old_price' : tuple(i[2] for i in items),
            'count' : tuple(i[3] for i in items),
            'wb_id' : tuple(i[4] for i in items),
            'wm_id' : tuple(i[5] for i in items),
            'wb_link' : tuple(i[6] for i in items),
            'wm_link' : tuple(i[7] for i in items),
            'sku' : tuple(i[8] for i in items),
            'cof' : tuple(i[9] for i in items),
            'category': tuple(i[10] for i in items)
        }
        self.con.close()
        return items_dict





class addNewItem(database):
    """ Класс для добавления новых товаров """
    def __init__(self, wm_id, wb_id, sku, cof, category):
        super().__init__()
        self._wm_id = wm_id
        self._wb_id = wb_id
        self._sku = sku
        self._cof = cof
        self._category = category

    """ Метод запускает парсер, который собирает информацию с WMart, создает list состоящий из
        информации с WMart, а так же из переданных агрументов в __init__. Вызывает функцию get_calculation_price()
        для расчета нужной для WB цены и добавляет этот list в базу данных"""
    def add_item(self):
        parser = parserConfig(f'https://wmart.kz/prod/{self._wm_id}/')
        wm_item_info = [i for i in parser.add_item_parse()]
        wm_item_info.append(self._wb_id)
        wm_item_info.append(self._wm_id)
        wm_item_info.append(f'https://www.wildberries.ru/catalog/{self._wb_id}/detail.aspx')
        wm_item_info.append(f'https://wmart.kz/prod/{self._wm_id}/')
        wm_item_info.append(self._sku)
        wm_item_info.append(self._cof)
        wm_item_info.append(self._category)

        wb_price = get_calculation_price(wm_item_info[1], self._cof, self._category, get_rate())

        wm_item_info.append(wb_price)

        self.cur.execute('INSERT INTO wb_wm(name, old_price, count, wb_id, wm_id, wb_link, wm_link, sku, cof, category, current_price) VALUES(?,?,?,?,?,?,?,?,?,?,?)', tuple(wm_item_info))
        self.con.commit()
        self.con.close()



class delItem(database):
    """ Класс для удаления товара из базы данных """
    def __init__(self):
        super().__init__()


    def del_item(self, wm_id):
        self.cur.execute('DELETE from wb_wm where wm_id=?', (wm_id,))
        print(wm_id)
        self.con.commit()
        self.con.close()



class wbDB(database):
    def add_price_wb(self, wb_id):
        return self.cur.execute('SELECT wb_id, current_price FROM wb_wm WHERE wb_id = ?', (wb_id,)).fetchone()


    def add_sku_count(self, wb_id):
        return self.cur.execute('SELECT sku, count FROM wb_wm WHERE wb_id = ?', (wb_id, )).fetchone()


    def update_items(self):
        return self.cur.execute('SELECT wm_id, wb_id, cof, category FROM wb_wm').fetchall()



class updateItemsDb(database):
    def update_item(self, price, count, wb_id):
        self.cur.execute('UPDATE wm_id SET current_price = ?, count = ? WHERE wb_id = ?', (price, count, wb_id))
        self.con.commit()
        self.con.close()