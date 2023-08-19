import socket
import json

from add_item_new import add_item
from file_manager_gui import contentWidgets


server = socket.socket()

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('192.168.0.2', 9090))
server.listen()


while True:
    conn, addr = server.accept()
    x = True
    msg = conn.recv(10000)
    json_reader = json.loads(msg)
    if json_reader.get('get'):
        print('server1')
        cw = contentWidgets()
        content = cw.get_content()
        print(content)
        json_post = json.dumps(content).encode('utf-8')
        conn.send(json_post)

    if json_reader.get('add'):
        add_item(json_reader['add']['wb_id'], json_reader['add']['wm_id'], json_reader['add']['sku'], json_reader['add']['cof'])

    if json_reader.get('del'):
        cw = contentWidgets()
        cw.del_item(json_reader['del']['wb_id'])
    if json_reader.get('update')
        cw = contentWidgets():
        cw.update_cof(json_reader['update']['wb_id'], json_reader['update']['cof'])

    conn.close()
