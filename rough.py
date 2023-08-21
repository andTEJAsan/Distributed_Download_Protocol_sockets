from threading import Thread
import socket
try:
    mySocket = socket.socket()
except Exception as e:
    print("Error in creating socket: ", e)
    exit(0)
port = 12345

#We will bind our process to this port
mySocket.bind(('', port))
#we have used an empty field as the first argument
#this means that we will accept connections from all IPs
#on the specified port
print("Socket binded to %s" %(port))   
#we will now listen for connections
mySocket.listen(5)
print("Socket is listening")

#we will now accept connections
#write a simple function that respnds to a connection
#with a hello message
def respond(conn : socket.socket):
    conn.send("Hello from server".encode())
    #what does the line below do?

    #it receives data from the client
    #the argument is the maximum number of bytes to be received
    #the return value is the data received
    while True:
        data_received = conn.recv(1024)
        print(data_received.decode())

def main():
    while True:
        try:
            conn, addr = mySocket.accept()
            print("Connection accepted from ", addr)
        except Exception as e:
            print("Error in accepting connection: ", e)
            continue
        print("Connection established with ", addr)
        Thread(target =respond, args = (conn,) ).start()

if __name__ == "__main__":
    main()
