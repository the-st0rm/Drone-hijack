#!/usr/bin/env python
import socket
import os



def main():
    
    TCP_IP = "10.7.23.99" #This is the IP of the pandaboard. It is better to get it from the ip.py file than hardcoding it

    TCP_PORT = 5555#the normal port of streaming video on the drone
    BUFFER_SIZE = 512  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)#listen on the pandaboard IP and 5555 port which is the video streaming port
    print "Server Listening on: " + TCP_IP + ":" +str(TCP_PORT)    
    while 1:
        conn, addr = s.accept()#once we accept the connection
        print "connection address: " + str(addr)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        drone_ip = '192.168.2.1'
        drone_port = 5555
        client.connect((drone_ip, drone_port)) #we connect to our drone
        while 1: 
            data = client.recv(BUFFER_SIZE) #recv data from the drone
            #print data
            conn.send(data) #send these data to the client connected to the panda board
        
    
    #We, simply, recieve data from the drone on ip 102.168.2.1 and we RELAY it to who ever connected to us on port 5555
    
    return


if __name__ == '__main__':
    main()
