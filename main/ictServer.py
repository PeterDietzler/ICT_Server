import utime
import os
import machine
import micropython
import builtins
import network
import socket
from main.main_website import web_page
from ota_update.ota_updater import OTAUpdater


class ictServer:

    def __init__(self, config_data):
        
        print('init ictServer()')
        
        print('Show Aktual main/.version ', self.get_version('main'))
        
        self.setAP = config_data["wifi"]["setAP"]
        print('setAP = ', self.setAP)
     
        #self.crate_Socket(config_data)
               
        self.ict_Loop_Funktion(config_data)
    
    
    def get_version(self, directory):
        if '.version' in os.listdir(directory):
            f = open(directory + '/.version')
            version = f.read()
            f.close()
            return version
        return '0.0'
    
    def open_Socket(self, config_data):
        print('open_Socket()')
        if config_data["wifi"]["setAP"] == 1:
            print('setAP (True) = ', self.setAP)
            AP_ssid     = config_data['wifi']['AP_ssid']
            AP_password = config_data['wifi']['AP_password']
            print('crate_AP_Socket()', AP_ssid, AP_password)
            
            ap = network.WLAN(network.AP_IF)
            ap.active(True)
            
            ap.config(essid=AP_ssid, password=AP_password)
            
            while not ap.active():
                pass
            print('network config:', ap.ifconfig())
            pass
        elif config_data["wifi"]["setAP"] == 0:
            print('setAP (Fals) = ', self.setAP)
            ssid     = config_data['wifi']['ssid']
            password = config_data['wifi']['password']
            print('crate_Socket()', ssid, password)
            sta = network.WLAN(network.STA_IF)
            if not sta.isconnected():
                print('connecting to network...')
                sta.active(True)
                sta.connect(ssid, password)
                while not sta.isconnected():
                    pass
            print('network config:', sta.ifconfig())
            
            
            print('config ota updater:')
            ota = OTAUpdater( config_data['wifi']['gitpath'] )
            print('Starte ota updater check:')
            result = ota.check_for_update_to_install_during_next_reboot()
            print('ota updater =', result)

            
            
            
            
            pass
        else:
            print('ERROR setAP = ', config_data["wifi"]["setAP"])
            return 0
        # AF_INET - use Internet Protocol v4 addresses
        # SOCK_STREAM means that it is a TCP socket.
        # SOCK_DGRAM means that it is a UDP socket.
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind(('',80)) # specifies that the socket is reachable by any address the machine happens to have
        soc.listen(5)     # max of 5 socket connections
        return soc        
    
   
    def ict_Loop_Funktion(self, config_data):
        print('====== ict_Loop_Funktion() =========')
        
        '''
        if config_data["wifi"]["setAP"] == 1:
            print('setAP (True) = ', self.setAP)
            AP_ssid     = config_data['wifi']['AP_ssid']
            AP_password = config_data['wifi']['AP_password']
            print('crate_AP_Socket()', AP_ssid, AP_password)
            
            ap = network.WLAN(network.AP_IF)
            ap.active(True)
            
            ap.config(essid=AP_ssid, password=AP_password)
            
            while not ap.active():
                pass
            print('network config:', ap.ifconfig())
            pass
        elif config_data["wifi"]["setAP"] == 0:
            print('setAP (Fals) = ', self.setAP)
            ssid     = config_data['wifi']['ssid']
            password = config_data['wifi']['password']
            print('crate_Socket()', ssid, password)
            sta = network.WLAN(network.STA_IF)
            if not sta.isconnected():
                print('connecting to network...')
                sta.active(True)
                sta.connect(ssid, password)
                while not sta.isconnected():
                    pass
            print('network config:', sta.ifconfig())
            pass
        else:
            print('ERROR setAP = ', config_data["wifi"]["setAP"])
            return 0
        # AF_INET - use Internet Protocol v4 addresses
        # SOCK_STREAM means that it is a TCP socket.
        # SOCK_DGRAM means that it is a UDP socket.
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind(('',80)) # specifies that the socket is reachable by any address the machine happens to have
        soc.listen(5)     # max of 5 socket connections
        '''
        soc = self.open_Socket(config_data)
        
        led = 0

        while True:
            # Socket accept() 
            conn, addr = soc.accept()
                        
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
                led = 1
            elif led_off == 6:
                print('LED OFF')
                print(str(led_off))
                led = 0
            response = web_page(led)
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)

            # Socket close()
            conn.close()
            
