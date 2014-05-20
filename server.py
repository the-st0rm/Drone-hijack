#!/usr/bin/env python
import socket
import os
import libardrone

if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                ifname[:15]))[20:24])

def get_lan_ip():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = [
            "eth0",
            "eth1",
            "eth2",
            "wlan0",
            "wlan1",
            "wifi0",
            "ath0",
            "ath1",
            "ppp0",
            ]
        ip = {}
        for ifname in interfaces:
            try:
                ip[ifname]= get_interface_ip(ifname)
            except IOError:
                pass
    return ip


def server(drone_ip='192.168.1.1', server_port=6666):
    #this function takes the drone ip and a port to connect to the drone on that ip
    #and listens on that port on the panda board to recieve any commands that will sent to control the drone
    TCP_IP = TCP_IP['eth0'] #getting the IP address of the panda board
    print TCP_IP
    TCP_PORT = server_port
    BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1) #listening on the panda board on port=6666 by default
    print "Server Listening on: " + TCP_IP + ":" +str(TCP_PORT)
    while 1:
        conn, addr = s.accept() #once we accept connection
        print "connection address: " + str(addr)
        var = 'Uninitialized'
        drone = libardrone.ARDrone(drone_ip) #We create a drone object. Now, we are connected to our drone
        while 1:
            

            #s=socket.socket(socket_AF_INET, socket.SOCK_STREAM)
            data = conn.recv(BUFFER_SIZE)  #recieving commands from the TCP connection and execute the corresponding commands on the drone
            if data == 'False':
                var = 'False' 
            elif data == 'hover':
                var = 'hover'
                drone.hover()
            elif data == 'K_ESCAPE':
                var='K_ESCAPE'
                drone.reset()
                # takeoff / land
            elif data == 'K_RETURN':
                var = 'K_RETURN'
                drone.takeoff()
            elif data == 'K_SPACE':
                var = 'K_SPACE'
                drone.land()
            # emergency
            elif data == 'K_BACKSPACE':
                var = 'K_BACKSPACE'
                drone.reset()
            # forward / backward
            elif data == 'K_w':
                var = 'K_w'
                drone.move_forward()
            elif data == 'K_q':
                var = 'K_q'
            elif data == 'K_s':
                var = 'K_s'
                drone.move_backward()
            # left / right
            elif data == 'K_a':
                var = 'K_a'
                drone.move_left()
            elif data == 'K_d':
                var = 'K_d'
                drone.move_right()
            # up / down
            elif data == 'K_UP':
                var = 'K_UP'
                drone.move_up()
            elif data == 'K_DOWN':
                var = 'K_DOWN'
                drone.move_down()
            # turn left / turn right
            elif data == 'K_LEFT':
                var = 'K_LEFT'
                drone.turn_left()
            elif data == 'K_RIGHT':
                var = 'K_RIGHT'
                drone.turn_right()
            if not data: break
            print "received data:", data
            print "var =  " + str(var)
            conn.send("echo: " + var)  # echo the command back for testing 
            if str(data)=='False':
                print "Cutting the connection"
                break
        

        drone.halt() #halt the drone
        conn.close() #close the connection
        break
    print "Ending the program"

if __name__ == '__main__':
    main()
