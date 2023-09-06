import sqlite3
from wb_api import post_amount, post_price


class fileManagerAdd:
    def __init__(self, values, wb_id, mw_id, mw_link, wb_link, sku, cof, category):
        self._values = values
        self._values.append(wb_id)
        self._values.append(mw_id)
        self._values.append(wb_link)
        self._values.append(mw_link)
        self._values.append(sku)
        self._values.append(cof)
        self._values.append(category)
        self._wb_tuple = (values[1],wb_id , values[3], sku, cof, category)

    #Подключение к DB
    def _sqlite_con(self):
        con = sqlite3.connect('WB_WM.db')
        cur = con.cursor()
        cur.execute('CREATE TABLE if not exists wb_wm(name, current_price, old_price, count, wb_id, wm_id, wb_link, wm_link, sku, cof)')
        table = cur.execute('PRAGMA table_info("wb_wm")').fetchall()[-1]
        if table[1] != 'category':
            cur.execute('ALTER TABLE wb_wm ADD column category "float" DEFAULT 0 ')
            cur.execute('UPDATE wb_wm SET category = 0')
        con.commit()
        return con

    def add_item(self):
        con = self._sqlite_con()
        cur = con.cursor()
        _to_tuple = tuple(self._values)
        cur.execute('INSERT INTO wb_wm(name, current_price, old_price, count, wb_id, wm_id, wb_link, wm_link, sku, cof, category)\
                     VALUES(?,?,?,?,?,?,?,?,?,?,?)', _to_tuple)

        con.commit()
        con.close()
        amount_tuple = [(self._wb_tuple[2], self._wb_tuple[3])]
        price_tuple = [(self._wb_tuple[0], self._wb_tuple[1])]
        post_amount(amount_tuple)
        post_price(price_tuple, [(self._wb_tuple[4],)], [(self._wb_tuple[5],)])


class fileManagerUpdate:
    def _sqlite_con(self):
        return sqlite3.connect('WB_WM.db')

    def get_links_for_update(self):
        con = self._sqlite_con()
        cur = con.cursor()
        self._price_link = cur.execute('SELECT wm_link FROM wb_wm').fetchall()
        return self._price_link

    def update_price_records(self, values_dict):
        con = self._sqlite_con()
        cur = con.cursor()
        sql_query = """Update wb_wm set current_price = ? where wm_link = ?"""
        records_list_price = [(v, k) for k, v in values_dict[0].items()]
        cur.executemany(sql_query, records_list_price)
        con.commit()
        sql_query = """Update wb_wm set count = ? where wm_link = ?"""
        records_list_count = [(v, k) for k, v in values_dict[1].items()]
        cur.executemany(sql_query, records_list_count)
        con.commit()
        nm_price = cur.execute('SELECT current_price, wb_id FROM wb_wm').fetchall()
        cof = cur.execute('SELECT cof FROM wb_wm').fetchall()
        category = cur.execute('SELECT category FROM wb_wm').fetchall()
        post_price(nm_price, cof, category)
        sku_count = cur.execute('SELECT count, sku FROM wb_wm').fetchall()
        post_amount(sku_count)

        con.close()
