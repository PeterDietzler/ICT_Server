#import builtins
import network
import usocket as socket


class myWiFi:

   def __init__(self):
        print('init myWiFi()')
        
        #self.setAP = config_data["wifi"]["setAP"]
        #print('setAP = ', self.setAP)

   def open_Socket_AP( self, ssid, password ):
        print('open_Socket_AP()', ssid, "***************")
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config( essid=ssid, password=password)

        while not ap.active():
            pass
        print('network config:', ap.ifconfig())
        # AF_INET - use Internet Protocol v4 addresses
        # SOCK_STREAM means that it is a TCP socket.
        # SOCK_DGRAM means that it is a UDP socket.
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind(('',80)) # specifies that the socket is reachable by any address the machine happens to have
        soc.listen(5)     # max of 5 socket connections
        return soc        

  
   def open_Socket_STA( self, ssid, password ):
        #TODO Scanne netzwerk ob bekante netze vorhanden
        #     -> ansonsten Access Point
        '''
        wlan_sta = network.WLAN(network.STA_IF)
        
        sList = wlan_sta.scan()
        print('Scan()', sList)
        for n in sList:
            print(' x= ', n)
        '''    
      
        print('crate_Socket()', ssid, "***************")
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
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.bind(('', 80)) # specifies that the socket is reachable by any address the machine happens to have
        soc.listen(5)      # max of 5 socket connections
        return soc        

   def open_Socket(self, config_data):
        print('open_Socket()')
        if config_data["wifi"]["setAP"] == 1:
            print('setAP (True) = ', self.setAP)
            AP_ssid     = config_data['wifi']['AP_ssid']
            AP_password = config_data['wifi']['AP_password']
            print('crate_AP_Socket()', AP_ssid, "***************")
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
            print('crate_Socket()', ssid, "***************")
            sta = network.WLAN(network.STA_IF)
            if not sta.isconnected():
                print('connecting to network...')
                sta.active(True)
                sta.connect(ssid, password)
                while not sta.isconnected():
                    pass
            print('network config:', sta.ifconfig())
            
            check_for_ota_update(config_data)
            #initTime()
            #getntptime()
            #get_ntp_time()
            resolve_dst_and_set_time()
            print('Current Time:', utime.localtime())
            
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
   
   def connect_WLAN_STA( self, ssid, password ):
        print('crate_Socket()', ssid, "***************")
        sta = network.WLAN(network.STA_IF)
        if not sta.isconnected():
            print('connecting to network...')
            sta.active(True)
            sta.connect(ssid, password)
            while not sta.isconnected():
                pass
        print('network config:', sta.ifconfig())
