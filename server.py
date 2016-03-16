#!/usr/bin/env python3

import io
import socket
import sys
import tarfile

port = int(sys.argv[1])

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', port))
serversocket.listen(1)


(clientsocket, address) = serversocket.accept()

class Nope(Exception):
    pass

try:
    SEP = b'\r\n\r\n'
    headers = b''
    headers_done = False
    body = b''

    chunk = clientsocket.recv(4096)
    while chunk != b'':
        if headers_done:
            sys.stdout.buffer.write(chunk)
            sys.stdout.buffer.flush()

            # body += chunk
            # try:
            #     for start in range(0, len(body)):
            #         for end in range(len(body), 0, -1):
            #             try:
            #                 tarfile.open(fileobj=io.BytesIO(body[start:end]), debug=3).list()
            #                 print('Successful range: %d -> %d' % (start, end))
            #                 raise Nope
            #             except tarfile.ReadError as e:
            #                 pass
            # except Nope:
            #     pass
        else:
            headers += chunk
            if SEP in headers:
                body = headers[headers.find(SEP) + len(SEP):]
                sys.stdout.buffer.write(body)
                sys.stdout.buffer.flush()
                headers_done = True

        chunk = clientsocket.recv(4096)
finally:
    clientsocket.close()
    serversocket.close()
