# -*- coding: utf-8 -*-
import sys
import os
from socket import *

FILE_PATH = str(sys.argv[1])
IP = "127.0.0.1"
RCV_PORT = int(sys.argv[2])
# N = int(sys.argv[2])
# RETRANSMISSION_TIMEOUT = int(sys.argv[4]) # in ms

udp_socket = socket(AF_INET, SOCK_DGRAM)
host = IP
addr = (host, RCV_PORT)
chunk_size = 1024  # 1 KiB

with open(FILE_PATH, "rb") as in_file:
    while True:
        chunk = in_file.read(chunk_size)
        udp_socket.sendto(chunk, addr)
        if chunk == b"":
            break  # end of file
