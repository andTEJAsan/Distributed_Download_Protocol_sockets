import socket
import threading as th
from threading import Thread
from threading import Lock
import time
import sys
#maybe for starting off we can output all the lines in the file that we read from the server and send those over.
##The basic variables we need to use for the thread that gets new data from the server sending the lines.

##Building a protocol for the data transfer.



###
"""I think the following protocol would work well. the client stores the last index of the lines it has received before, 
and when it asks for an update, we only send the new lines added to our list after this particular index. But we have to be careful about the fact that some of those lines might have come from the client to us before
"""
"""Another thing we can do is that we only send the line numbers through the socket, and then send the line only if the client replies back that it wants those lines."""
hash_lines = [-1]*1002; #this is the hash of the lines that we have received so far.
all_my_lines = []; 
all_lines = []; 
all_lines_lock = Lock(); 
all_my_lines_lock = Lock(); 
hash_lines_lock = Lock(); 
total_lines = 1000; #for now.

def send_data(socket, data):
    #the protocol to send anything to the server is simple. We first send it the number of bytes to receive and then the data, so the 
    #receiving end knows how much data to receive, and when to stop the recv loop. 
    data = data.encode(); 
    socket.send((str(len(data)) + '\r').encode()); #sends the number of bytes to receive.
    socket.send(data); #sends the data itself.

def receive_data(socket):
    #the protocol to receive anything from the server is simple. We first receive the number of bytes to receive and then the data, so the 
    #receiving end knows how much data to receive, and when to stop the recv loop. 
    first_recv = socket.recv(1024).decode(); #receives the number of bytes to receive.
    totalData = first_recv.split('\r');
    try:
        bytes_to_receive = int(totalData[0]); #the part before the \r
    except Exception as e:
        print("first_recv: ", first_recv, " totalData: ", totalData, " exception: ", e);
        return None; 

    if(len(totalData) > 1):
        totalData = "".join(totalData[1:]); #the part after the \r
        bytes_to_receive -= len(totalData.encode());
    else:
        totalData = ""; 
    string_data_array = [];
    while(bytes_to_receive > 0):
        data = socket.recv(bytes_to_receive);
        string_data_array.append(data.decode());
        bytes_to_receive -= len(data); 
    totalData += "".join(string_data_array);
    # print("received: ", totalData, " from socket ", socket); 
    return totalData;



def getLinesFromServer(s): #s is the socket.
    send_data(s, "GET\n"); #we send the get request to the server.
    data = receive_data(s).split('\n'); #we receive the data from the server.
    #now we need to check in our current list if we have this particular data and if we do not then we should add this.
    with all_lines_lock:
        with hash_lines_lock: 
            l = len(data); 
            for i in range(0,l,2):
                if(hash_lines[int(data[i])] == -1):
                    newLine = data[i] + "\n" + data[i+1] + "\n";
                    all_lines.append(newLine); 
                    hash_lines[int(data[i])] = 1; #we have seen this line now.


def clientThread(csocket, addr):
    lastCall = 0; #the last call that the client made to the server.
    while True:
        # print("client ", addr, " connected"); 
        decoded_response = receive_data(csocket); #we receive the data from the client.
        #decoded_response = response.decode(); 
        if(decoded_response):
            r = decoded_response.split(); 
            if(r[0] == "GET" or r[0] == "GET\n"):
                from_index = lastCall; #then we should return the new lines we found from the index mentioned.
                data = []; 
                #with all_lines_lock: #perhaps this lock is actually not required though. but lets keep it for now. 
                end_index = len(all_lines); 
                for i in range(from_index, end_index): 
                    data.append(all_lines[i]);
                data = ''.join(data);
                lastCall = end_index; 
                send_data(csocket, data); #we send the data to the client.
    csocket.close(); 

def mainThread():
    errors = 0; 
    mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mainSocket.connect(("vayu.iitd.ac.in", 9801));
    sendline = "SENDLINE\n".encode(); 
    while(True):
        mainSocket.send(sendline); #gets a line from the server.
        try:
            line = mainSocket.recv(10000).decode(); 
            # line = receive_data(mainSocket); 
            lineNumber = int(line.split('\n')[0]); #to get the line number.
        except Exception as e:
            #print(line + ":: raised the error " + str(e));
            #raise e; #since this error is not expected to happen.
            errors += 1;
            continue;
        if(lineNumber == -1):
#            getLinesFromServer(server1); 
            continue; #not a useful result for us, we can just continue;.
        # with all_lines_lock:
        #     with hash_lines_lock:
        #         with all_my_lines_lock:
        if(hash_lines[lineNumber] == -1):
            hash_lines[lineNumber] = line; #so we update this line in our hashset, while also adding this to our list of lines.
            all_lines.append(line); 
            all_my_lines.append(line); 
            print(len(all_lines), " total lines done", "added line: ", lineNumber); 
        if(len(all_lines) >= total_lines):
            break; #since we have reached the end and all the lines have been read.
    print("total errors: ", errors);




def myServer(port = 12345):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); 
    s.bind(('', port))        
    print ("socket binded to %s" %(port))
    # put the socket into listening mode
    s.listen(4) #backlog 4      
    connections = 0;
    while connections < 1: #forever keeps looping
        # Establish connection with client.
        client, addr = s.accept() 
        connections += 1; #after the above acception   
        #running this in a completely new thread.
        Thread(target = clientThread, args = (client, addr)).start(); 
        #time.sleep(0.1); #so that the client can connect to the server.
# Thread(target = mainThread()).start(); 
if __name__ == "__main__":
    Thread(target = myServer(), args = ()).start(); 
    if(len(sys.argv) > 1):
        server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM); 
        server1.connect(sys.argv[1], 12345); #connects to the server running at this ip.
    Thread(target = mainThread(), args = ()).start(); 

