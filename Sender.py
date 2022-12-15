# -*- coding: utf-8 -*-
import sys
import os
from socket import *
import threading
import time

IP = "127.0.0.1"
FILE_PATH = str(sys.argv[1])
RCV_PORT = int(sys.argv[2])
N = int(sys.argv[3])
RETRANSMISSION_TIMEOUT = int(sys.argv[4])  # in ms

udp_socket = socket(AF_INET, SOCK_DGRAM)
host = IP
addr = (host, RCV_PORT)
chunk_size = 1022  # 1 KiB
rcved_acks = {}
thread_arr = list()


def run():
    time.sleep(0.05)
    if not udp_socket.recv(
            chunk_size):  # ack için başka bişey var mı yoksa direkt recv mi kullancaz/ argument emin degilim
        run()

def rcv_ack():
    print('wait for ack')
    while len(rcved_acks) != packet_no_counter:
        ack = udp_socket.recv(chunk_size)
        print('ack rcved ==>  ' + str(ack))
        int_val_ack = int.from_bytes(ack, "big")
        if thread_arr[int_val_ack - 1].is_alive():
            print('Thread ' + str(int_val_ack) + ' is joined.')
            thread_arr[int_val_ack - 1].join()

def sendData(packet, packet_no):
    while True:
        print(rcved_acks)
        if packet_no in thread_arr:  # main process threadleri kapattığı için buna gerek olmayabilir bakmak lazım
            break
        udp_socket.sendto(packet, addr)

        time.sleep(RETRANSMISSION_TIMEOUT / 1000.0)


packet_no_counter = 1
print('Start sending')
ack_thread = threading.Thread(target=rcv_ack, args=())
ack_thread.start()

with open(FILE_PATH, "rb") as in_file:
    while True:
        chunk = in_file.read(chunk_size)
        header = bytearray(packet_no_counter.to_bytes(2, 'big'))
        if chunk == b"":
            end_pointer = bytearray((0).to_bytes(2, 'big'))
            end_pointer += bytearray(chunk)

            udp_socket.sendto(end_pointer, addr)
            print('--FILE SEND IS END--- ' + str(packet_no_counter))
            break  # end of file

        header += bytearray(chunk)

        new_thread = threading.Thread(target=sendData, args=(header, packet_no_counter))
        thread_arr.append(new_thread)
        thread_arr[packet_no_counter - 1].start()
        packet_no_counter = packet_no_counter + 1
        time.sleep(1)


