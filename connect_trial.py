#!/usr/bin/env python3
import argparse
import socket
from A2final import send_data,receive_data
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
parser = argparse.ArgumentParser()
parser.add_argument("ip",type=str, help="ip address of the server")
parser.add_argument("port",type=int, help="port number of the server")

args = parser.parse_args()
ip = args.ip
port = args.port
s.connect((ip, port))
while True:
    msg = input()
    send_data(s,msg)
    print(receive_data(s))