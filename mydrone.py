import server
import sys

if len(sys.argv) < 3:
    print "Usage is filename <ip> <port>"
    exit()

ip = sys.argv[1]
port = int(sys.argv[2])

#connect to my drone that is on IP =ip and open a port on the panda board to listen to my commands
#the panda board recieves my commands on the port passed to the server function and relay this commands to the real drone

server.server(ip, port)
