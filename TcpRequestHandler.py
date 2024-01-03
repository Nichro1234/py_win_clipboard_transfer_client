import ClipboardManager
from config import X_API_VERSION, AUTHKEY

import json
import time


def parse_request(request):
    raw_list = request.split("\r\n")
    request_params = {}
    for index in range(1, len(raw_list)):
        item = raw_list[index].split(":")
        if len(item) == 2:
            request_params.update({item[0].lstrip(' '): item[1].lstrip(' ')})
    return request_params


def tcp_link(sock, addr):
    # since we know there is less than 1024 bytes
    data = sock.recv(1024)
    result = data.decode()
    print(parse_request(result))

    # response
    http_head = 'HTTP/1.1 200 ok\r\nContent-Type: application/json; charset=utf-8\r\n\r\n'
    data = ClipboardManager.get_clipboard()
    data = json.dumps(data)
    sock.send((http_head + data).encode())

    sock.close()
