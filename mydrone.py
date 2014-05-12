import server
import sys

if len(sys.argv) < 3:
    print "Usage is filename <ip> <port>"
    exit()

ip = sys.argv[1]
port = int(sys.argv[2])

server.server(ip, port)
