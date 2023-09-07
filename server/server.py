import socket
import json

from add_item_new import add_item
from file_manager_gui import contentWidgets


server = socket.socket()

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('109.248.170.187', 9090))
server.listen()

while True:
    conn, addr = server.accept()
    x = True
    msg = conn.recv(10000)
    if msg != None:
        try:
            json_reader = json.loads(msg)
        except Exception as e:
            print(e)
        if json_reader.get('get'):
            cw = contentWidgets()
            content = cw.get_content()
            json_post = json.dumps(content).encode('utf-8')
            print(json_post)
            conn.sendall(json_post)

        if json_reader.get('add'):
            add_item(json_reader['add']['wb_id'], json_reader['add']['wm_id'], json_reader['add']['sku'], json_reader['add']['cof'], json_reader['add']['category'])

        if json_reader.get('del'):
            cw = contentWidgets()
            cw.del_item(json_reader['del']['wb_id'])
        if json_reader.get('update_cof'):
            cw = contentWidgets()
            cw.update_cof(json_reader['update_category']['wb_id'], json_reader['update_category']['cof'])
        if json_reader.get('update_category'):
            cw = contentWidgets()
            cw.update_category(json_reader['update_category']['wb_id'], json_reader['update_category']['category'])
        else:
            continue
    conn.close()
