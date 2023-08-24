#!/usr/bin/env python3
import argparse
import sys
import socket
from A2final import send_data, receive_data
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = sys.argv[1]
port = int(sys.argv[2]);
s.connect((ip, port))
while True:
    msg = input()
    send_data(s,msg)
    print(receive_data(s)); 