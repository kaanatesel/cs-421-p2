# -*- coding: utf-8 -*-
import sys
import os
from socket import *
import threading
import time

FILE_PATH = str(sys.argv[1])
IP = "127.0.0.1"
RCV_PORT = int(sys.argv[2])
# N = int(sys.argv[2])
# RETRANSMISSION_TIMEOUT = int(sys.argv[4]) # in ms

udp_socket = socket(AF_INET, SOCK_DGRAM)
host = IP
addr = (host, RCV_PORT)
chunk_size = 1022  # 1 KiB


def run():
    time.sleep(0.05)
    if not udp_socket.recv(chunk_size):  #ack için başka bişey var mı yoksa direkt recv mi kullancaz/ argument emin degilim
        run()


packet_no_counter = 1
with open(FILE_PATH, "rb") as in_file:
    while True:
        chunk = in_file.read(chunk_size)
        header = bytearray(packet_no_counter.to_bytes(2, 'big'))
        if chunk == b"":
            end_pointer = bytearray((0).to_bytes(2, 'big'))
            end_pointer += bytearray(chunk)

            udp_socket.sendto(end_pointer, addr)
            sending = threading.Thread(run())
            print('--FILE SEND IS END--- ' + str(packet_no_counter))
            break  # end of file

        header += bytearray(chunk)
        udp_socket.sendto(header, addr)
        packet_no_counter = packet_no_counter + 1
