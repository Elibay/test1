import sqlite3
import requests

class contentWidgets:
    def _sqlite_con(self):
        return sqlite3.connect('WB_WM.db')

    def get_content(self):
        cur = self._sqlite_con().cursor()
        cur.execute('CREATE TABLE if not exists wb_wm(id INTEGER PRIMARY KEY AUTOINCREMENT,\
                    name STRING, current_price INTEGER, old_price INTEGER, count INTEGER, wb_id INTEGER,\
                     wm_id INTEGER, wb_link STRING, wm_link STRING, sku STRING, cof REAL)')

        items = cur.execute('SELECT name, current_price, old_price, count,\
                            wb_id, wm_id, wb_link, wm_link, sku, cof  FROM wb_wm').fetchall()

        rate = round(100 / requests.get(url='https://www.cbr-xml-daily.ru/daily_json.js')\
                   .json()['Valute']['KZT']['Value'], 1)
        items_dict = {
            'name' : tuple(i[0] for i in items),
            'current_price' : tuple(i[1] for i in items),
            'old_price' : tuple(i[2] for i in items),
            'count' : tuple(i[3] for i in items),
            'wb_id' : tuple(i[4] for i in items),
            'wm_id' : tuple(i[5] for i in items),
            'wb_link' : tuple(i[6] for i in items),
            'wm_link' : tuple(i[7] for i in items),
            'sku' : tuple(i[8] for i in items),
            'cof' : tuple(i[9] for i in items),
            'rate': rate
        }

        return items_dict
    def update_cof(self, wb_id, cof):
        con = self._sqlite_con()
        cur = con.cursor()
        cur.execute('UPDATE wb_wm set cof = ? where wb_id =?', (cof, wb_id))
        con.commit()
        con.close()
    
    def del_item(self, wb_id):
        with self._sqlite_con() as con:
            cur = con.cursor()
            cur.execute('DELETE from wb_wm where wb_id=?', (wb_id,))
