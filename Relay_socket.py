#!/usr/bin/env python
import socket
import os



def main():
    
    TCP_IP = "10.7.23.99"
    TCP_PORT = 5555
    BUFFER_SIZE = 512  # Normally 1024, but we want fast response

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)
    print "Server Listening on: " + TCP_IP + ":" +str(TCP_PORT)    
    while 1:
        conn, addr = s.accept()
        print "connection address: " + str(addr)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        drone_ip = '192.168.2.1'
        drone_port = 5555
        client.connect((drone_ip, drone_port))
        while 1: 
            data = client.recv(BUFFER_SIZE)
            #print data
            conn.send(data)
        
    
    
    
    return


if __name__ == '__main__':
    main()
