# -*- coding: utf-8 -*-
import sys
import os
from socket import *
import threading
import time

FILE_PATH = str(sys.argv[1])
IP = "127.0.0.1"
RCV_PORT = int(sys.argv[2])
N = int(sys.argv[3])
RETRANSMISSION_TIMEOUT = int(sys.argv[4])  # in ms

udp_socket = socket(AF_INET, SOCK_DGRAM)
host = IP
addr = (host, RCV_PORT)
chunk_size = 1022  # 1 KiB

rcved_acks = {}
send_packets = list()
thread_arr = list()


def run():
    time.sleep(0.05)
    if not udp_socket.recv(chunk_size):
        run()


def send_packet(packet, packet_no):
    print('rcv ack  ' + str(rcved_acks))
    while True:
        if packet_no in thread_arr:  # main process threadleri kapattığı için buna gerek olmayabilir bakmak lazım
            break
        udp_socket.sendto(packet, addr)

        time.sleep(RETRANSMISSION_TIMEOUT / 1000.0)


def is_file_trans_over(chunk):
    if chunk == b"":
        print('--FILE SEND IS END--- ' + str(packet_no_counter))
        end_pointer = bytearray((0).to_bytes(2, 'big'))
        end_pointer += bytearray(chunk)
        while True:
            ack = udp_socket.recv(chunk_size)
            print('ack rcved ==>  ' + str(ack))
            int_val_ack = int.from_bytes(ack, "big")
            print(ack)
            print(int_val_ack)
            if int_val_ack > 0:
                break

        udp_socket.sendto(end_pointer, addr)
        return True


packet_no_counter = 1
seq_no = 1
with open(FILE_PATH, "rb") as in_file:
    while True:
        chunk = in_file.read(chunk_size)
        if is_file_trans_over(chunk):
            break

        seq_no = packet_no_counter
        for seq_no in range(packet_no_counter, packet_no_counter + N - 1):
            print("seq nooo ==  " + str(seq_no))
            if len(thread_arr) == 0 or seq_no not in send_packets:
                print('in')
                header = bytearray(packet_no_counter.to_bytes(2, 'big'))
                header += bytearray(chunk)

                new_thread = threading.Thread(target=send_packet, args=(header, packet_no_counter))
                thread_arr.append(new_thread)
                #print(thread_arr)
                thread_arr[seq_no - 1].start()

                send_packets.append(packet_no_counter)

                seq_no = seq_no + 1
            else:
                print('already sent ' + str(seq_no))

        print(thread_arr)
        ack = udp_socket.recv(chunk_size)
        print('ack rcved ==>  ' + str(ack))
        int_val_ack = int.from_bytes(ack, "big")
        rcved_acks[int_val_ack - 1] = True

        if rcved_acks[packet_no_counter - 1]:
            packet_no_counter = packet_no_counter + 1

        if thread_arr[int_val_ack - 1].is_alive():
            print('Thread ' + str(int_val_ack) + ' is joined.')
            print(thread_arr[int_val_ack - 1])
            thread_arr[int_val_ack - 1].join()
