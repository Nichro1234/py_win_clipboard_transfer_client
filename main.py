import socket
import threading
import os

import pystray
from PIL import Image
from TcpRequestHandler import *

icon = Image.open("assets/img/file.ico")
start_on_boot = False


def on_click(_app, item):
    global start_on_boot
    start_on_boot = not item.checked


def exit_app(_app, item):
    _app.stop()
    os._exit(-1)


app = pystray.Icon("剪贴板助手")
app.menu = (
    pystray.MenuItem("开机启动", on_click,
                     checked=lambda item: start_on_boot),
    pystray.MenuItem("退出", exit_app)
)

app.icon = icon
app.run_detached()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 8086))
s.listen(5)
print('Waiting for connection...')


while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcp_link, args=(sock, addr))
    t.start()
