# -*- coding: utf-8 -*-
import sys
import os
from socket import *
import threading
import time
from math import ceil

FILE_PATH = str(sys.argv[1])
IP = "127.0.0.1"
RCV_PORT = int(sys.argv[2])
N = int(sys.argv[3])
RETRANSMISSION_TIMEOUT = int(sys.argv[4])  # in ms

udp_socket = socket(AF_INET, SOCK_DGRAM)
host = IP
addr = (host, RCV_PORT)
chunk_size = 1022  # 1 KiB

rcved_acks = set()
send_packets = set()
thread_arr = list()


def send_packet(packet, packet_no):
    # print('rcv ack  ' + str(rcved_acks))
    global rcved_acks, send_base
    while True:
        if packet_no in rcved_acks:
            break
        udp_socket.sendto(packet, addr)

        time.sleep(RETRANSMISSION_TIMEOUT / 1000.0)


def is_file_trans_over(chunk):
    global not_finshed, next_seq_no, rcved_acks
    file_size = os.path.getsize(FILE_PATH)
    packet_count = ceil(file_size / chunk_size)
    if chunk == b"":
        print('--FILE SEND IS END--- ' + str(next_seq_no))
        end_pointer = bytearray((0).to_bytes(2, 'big'))
        end_pointer += bytearray(chunk)
        udp_socket.sendto(end_pointer, addr)
        while True:
            # print('acks ' + str(len(rcved_acks)))
            # print(rcved_acks)
            #
            # print('packet_count ' + str(packet_count))
            if len(rcved_acks) + 1 >= packet_count:
                not_finshed = False
                break
        return True


not_finshed = True


def wait_ack():
    global rcved_acks, send_base, not_finshed
    while not_finshed:
        #print(not_finshed)

        ack = udp_socket.recv(chunk_size)
        int_val_ack = int.from_bytes(ack, "big")
        rcved_acks.add(int_val_ack)
        # print('send_base  ' + str(send_base))
        # print('int_val_ack  ' + str(int_val_ack))
        # print('thread_arr[int_val_ack - 1].is_alive():  ' + str(thread_arr[int_val_ack - 1].is_alive()))
        # print(str(rcved_acks))
        # print(thread_arr)
        # print(len(thread_arr))
        if int_val_ack in range(send_base, send_base + N):
            if thread_arr[int_val_ack - 1].is_alive():
                # print('Thread ' + str(int_val_ack) + ' is joined.')
                send_base = send_base + 1
                thread_arr[int_val_ack - 1].join()


wait_ack_thrd = threading.Thread(target=wait_ack)
wait_ack_thrd.start()

print('started')

in_file = open(FILE_PATH, "rb")

send_base = 1
next_seq_no = 1
while True:
    # print('next_seq_no  ' + str(next_seq_no) + '   send_base + N ' + str(send_base + N))
    # print('send_base + N ' + str(send_base + N))
    if next_seq_no <= send_base + N:
        chunk = in_file.read(chunk_size)

        if is_file_trans_over(chunk):
            print('end')
            break

        header = bytearray(next_seq_no.to_bytes(2, 'big'))
        header += bytearray(chunk)

        new_thread = threading.Thread(target=send_packet, args=(header, next_seq_no))
        thread_arr.append(new_thread)
        # print(thread_arr)
        thread_arr[next_seq_no - 1].start()
        next_seq_no = next_seq_no + 1

print('Finito')
exit()
wait_ack_thrd.join()
