import socket
import time
import sys

mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mainSocket.connect(("vayu.iitd.ac.in", 9801));
totalTries = 1;
if(len(sys.argv) > 2):
    totalTries = int(sys.argv[2]);
sendline = "SENDLINE\n".encode(); 
linesToRead = 1000;
if(len(sys.argv) > 1):
    linesToRead = int(sys.argv[1]);
errors = 0;
maxLimit = 10000; 
sumCounts = 0; 
for i in range(totalTries):
    startTime = time.time(); 
    done = set(); 
    allLines = [];
    cnt = 0;
    while(len(done) < linesToRead and cnt <= maxLimit):
        mainSocket.send(sendline); 
        line = mainSocket.recv(100000).decode();
        try:
            number = int(line.split('\n')[0]);
        except Exception as e:
            print(line + ":: raised the error " + str(e));
            raise e; 
            errors+=1; 
            continue; 
        if(number == -1):
            continue; 
        if(number not in done):
            done.add(number);
            allLines.append(line);
        cnt += 1;
        if(cnt % 100 == 0 and totalTries == 1):
            print("{0} calls done, {1} lines found, {2} curLine".format(cnt, len(done), number));
    endTime = time.time();
    print("time taken for " + str(len(done)) + " lines: " + str(endTime - startTime) + " with total errors: " + str(errors)); 
    result = "SUBMIT\n2021CS10556@QuickFetchers\n" + str(linesToRead) + "\n" + ''.join(allLines);
    mainSocket.send(result.encode());
    result = mainSocket.recv(100000).decode();
    print(result); 
    sumCounts += cnt;
    print(cnt, " calls, average so far: ", sumCounts/(i+1)); 

mainSocket.close(); 
