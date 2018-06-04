#!/usr/bin/env python3
#encoding: UTF-8
import time
from socket import *

HOST = gethostbyname(gethostname())
PORT = 4300
VERSION = '0.0.1'

if __name__ == "__main__":
    # create an INET, DATAGRAMing socket
    client_sckt = socket(AF_INET, SOCK_DGRAM)
    x = 0
    msg_req = ""
    client_sckt.sendto(msg_req.encode(), (HOST, PORT))
    (msg_resp, server_addr) = client_sckt.recvfrom(2048)
    print(msg_resp.decode())

    while True:
        if x == 0:
            msg_req = input('Enter a country or BYE to quit \n')
            x = 1
        else:
            msg_req = input('Enter another country or BYE to quit \n')

        client_sckt.sendto(msg_req.encode(), (HOST, PORT))
        (msg_resp, server_addr) = client_sckt.recvfrom(2048)

        print(msg_resp.decode())
        if msg_resp.decode() == "BYE":
            break

    client_sckt.close()