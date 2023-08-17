import socket

#from add_item_new import add_item
#from file_manager_gui import contentWidgets



HOST = (socket.gethostname(), 9090)

sock = socket.socket()

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(HOST)
sock.listen()
print('hello')


while True:
    conn, addr = sock.accept()
    print('connected - ', addr)

    res = b'Hello, my friend'
    conn.send(res)
    conn.close()

def add_item_new(wb_id, wm_id, sku):
    add_item(wb_id, wm_id, sku)

def delete_item(wb_id):
    cw = contentWidgets()
    cw.del_item(wb_id)


def get_content():
    cw = contentWidgets()
    content = cw.get_content()
    return content