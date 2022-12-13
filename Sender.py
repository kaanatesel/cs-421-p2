# -*- coding: utf-8 -*-
import sys
import os
from socket import *

FILE_PATH = str(sys.argv[1])
IP = "127.0.0.1"

# RCV_PORT = int(sys.argv[1])
# N = int(sys.argv[2])
# RETRANSMISSION_TIMEOUT = int(sys.argv[4]) # in ms

print(FILE_PATH)
file = open(FILE_PATH, 'rb')
# get the cursor positioed at end
file.seek(0, os.SEEK_END)
# get the current position of cursor
# this will be equivalent to size of file
print("Size of file is :", file.tell(), "bytes")

s = socket(AF_INET, SOCK_DGRAM)
host = IP
port = 9999
buf = 1024
addr = (host, port)

data = file.read(buf)
chunk_size = 1024  # 1 KiB

with open(FILE_PATH, "rb") as in_file, open("out-file.png", "wb") as out_file:
    while True:
        chunk = in_file.read(chunk_size)

        if chunk == b"":
            break  # end of file

        out_file.write(chunk)
