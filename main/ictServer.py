import utime
import os
import machine
import micropython
import builtins
import network
import main_website


class ictServer:

    def __init__(self, config_data):
        print('Show Aktual Version ', self.get_version('main'))
		self.setAP = config_data['wifi']['setAP']
		self.soc = 0
		crate_Socket(config_data):
		ict_Loop_Funktion(config_data):
    
    def get_version(self, directory):
        if '.version' in os.listdir(directory):
            f = open(directory + '/.version')
            version = f.read()
            f.close()
            return version
        return '0.0'
	
	def crate_Socket(self, config_data):
		if self.setAP == True:
			ssid     = config_data['wifi']['ssid']
			password = config_data['wifi']['pasword']
			ap = network.WLAN(network.AP_IF)
			ap.active(True)
			ap.config(ssid, password)
			while not ap.active():
				pass
			print('network config:', ap.ifconfig())
			# AF_INET - use Internet Protocol v4 addresses
			# SOCK_STREAM means that it is a TCP socket.
			# SOCK_DGRAM means that it is a UDP socket.
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind(('',80)) # specifies that the socket is reachable by any address the machine happens to have
			s.listen(5)     # max of 5 socket connections
		else:
			ssid     = config_data['wifi']['ssid']
			password = onfig_data['wifi']['pasword']
			sta = network.WLAN(network.STA_IF)
			if not sta.isconnected():
				print('connecting to network...')
				sta.active(True)
				sta.connect(ssid, password)
				while not sta.isconnected():
					pass
			print('network config:', sta.ifconfig())
			# AF_INET - use Internet Protocol v4 addresses
			# SOCK_STREAM means that it is a TCP socket.
			# SOCK_DGRAM means that it is a UDP socket.
			self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.soc.bind(('',80)) # specifies that the socket is reachable by any address the machine happens to have
			self.soc.listen(5)     # max of 5 socket connections

	
	def ict_Loop_Funktion(self, config_data):
		while True
			# Socket accept() 
			conn, addr = self.soc.accept()
			print("Got connection from %s" % str(addr))

			# Socket receive()
			request=conn.recv(1024)
			print("")
			print("")
			print("Content %s" % str(request))

			# Socket send()
			request = str(request)
			led_on = request.find('/?LED=1')
			led_off = request.find('/?LED=0')
			if led_on == 6:
				print('LED ON')
				print(str(led_on))
				led.value(1)
			elif led_off == 6:
				print('LED OFF')
				print(str(led_off))
				led.value(0)
			response = web_page()
			conn.send('HTTP/1.1 200 OK\n')
			conn.send('Content-Type: text/html\n')
			conn.send('Connection: close\n\n')
			conn.sendall(response)

			# Socket close()
			conn.close()
    
