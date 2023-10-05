import socket
import sys
from threading import Thread
from time import sleep
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip = sys.argv[1]
port = 12345; 
servers = [];

def clientThread(client, addr):
    while(True):
        try:
            msg = client.recv(1024).decode(); 
        except(socket.error):
            print("error receiving"); 
            continue; 
        if(msg == ""):
            print("client disconnected"); 
            break; 
        print("received: ", msg); 
        client.send(msg.encode());

def connect_servers(ports = 12345):
    total_connections = 1; 
    connections_made = 0; 
    while(connections_made < total_connections):
        try:
            server_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM); 
            servers.append(server_instance);
            servers[connections_made].connect((ip, port)); #connects to the server running at this ip.
        except:
            print("trying to connect to ", ports); 
            continue;
        connections_made += 1; ports += 1;
        print("connected to server at ", sys.argv[connections_made]); 
Thread(target = connect_servers, args = ()).start();
def myServer(port = 12345, total_connections = 1):
    connections = 0; 
    while connections < total_connections: #forever keeps looping
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); 
        s.bind(('', port))      
        print ("socket binded to %s" %(port))
        port+=1; #for the next one.
        # put the socket into listening mode
        s.listen(4) #backlog 4      
            # Establish connection with client.
        try:
            client, addr = s.accept() 
        except:
            print("didn't connect"); 
            sleep(0.1);
            continue; 
        connections += 1; #after the above acception   
        #running this in a completely new thread.
        print("connected to ", addr); 
        Thread(target = clientThread, args = (client, addr)).start(); 


while True:
    msg = input()
    s.send(msg.encode())
    print(s.recv(1024).decode()); 