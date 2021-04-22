try: # Micropython
    import utime
    import machine
    from machine import RTC
    import micropython
    import usocket as socket
    import ntptime
except:
    import socket
    import time
    pass

import os
import builtins
import network
#from .main_website import web_page
#from ota_update.ota_updater import OTAUpdater

from main.get_ntp_time import resolve_dst_and_set_time
#from main.myWifi.myWiFi import myWiFi
from main.WWW.myWiFiManager import myWiFiManager
from main.mylibs.myWiFi import myWiFi
from main.mylibs.shelly import shelly
from main.mylibs.iobroker import iobroker
global my_soc


def set_Brauchwasser_Heitzunng():
    # --------  WAS IST ZU BEACHTEN  ---------
    # 1. wenn Speicher Temperatur kleiner 45°C einschalten
    # 2. wenn Speicher Temperatur groeser 50°C ausschalten
    # 3. Uhrzeit beachten zwische 22:00 und 5:00 Uhr ausschalten
    #    ( ergibt sich möglicherweise schon aus den anderen Anforderungen)
    # 4. wenn die Heitzung sowiso gerade an ist lohnt das elektrische Heitzen nicht
    # 5. Wenn die Ausentemperatur kleiner 15°C wird die Heitzung sowiso an gehen
    # 6. Wenn kein PV-Überschuss da ist ausschlten
    # 7. Wenn PV-Überschuss vorhanden ist Modulierend heitzen -> Heitzleistung 0-100%
    #    (dh. kann trotzdem auch 2 Stufig geschalte werden:
    #    30%< =1000W; 30%-60%=2000W; 60% > =3000 )
    pass

def check_for_ota_update(config_data):
    print('Starte ota updater check:')
    ota = OTAUpdater( config_data['wifi']['gitpath'] )
    result = ota.check_for_update_to_install_during_next_reboot()
    #print('ota updater =', result)

def my_map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

	# Plugstat gibt an ob ein Stecker steckt,
	# Rückgabe ist jeweils 0 oder 1.
def get_plugstat():
    return 1

    # Chargestat gibt an, ob EVSEseitig die Ladung aktiv ist
    # Rückgabe ist jeweils 0 oder 1.
def get_chargestat():
    return 1

def get_State_Of_Charge():
    return my_soc

def set_State_Of_Charge(state_of_charge):
    global my_soc
    
    my_soc = state_of_charge
    return my_soc

def set_charge_current( current):
    print('set_charge_current():', current)
    return current
    
    
def getRequest( Value ):
    html_page = str(Value)  
    return html_page

class ictServer:

    def __init__(self, config_data):
        print('init ictServer()')
        self.setAP = config_data["wifi"]["setAP"]
        print('setAP = ', self.setAP)
        #wifi = myWiFiManager()
        #wifi.init_WiFiManager()

        ssid     = config_data['wifi']['ssid']
        password = config_data['wifi']['password']
        wifi= myWiFi()
        wifi.connect_WLAN_STA( ssid, password)  

        evu_energie       ='http://iobroker01:8087/getPlainValue/node-red.0.Haus.TotalEnergie'
        iob=iobroker()
        iob.get_raw( evu_energie)
        print('evu_energie = ', iob.get_raw( evu_energie))

        #ip_Heitzung     = '192.168.188.36' # Heizung tempeaturen
        #heitzung = shelly(ip_Heitzung)
        #bw_temp = heitzung.get_temperature( 2)
        #print('bw_temp     = ',bw_temp)
 
        self.ict_Loop_Funktion(config_data)

    def ict_Loop_Funktion(self, config_data):
        print('====== ict_Loop_Funktion() =========')
        if self.setAP == 1:
            ssid     = config_data['wifi']['AP_ssid']
            password = config_data['wifi']['AP_password']
            wifi= myWiFi()
            soc = wifi.open_Socket_AP( ssid, password)  
            print('soc:', soc)
        else:
            ssid     = config_data['wifi']['ssid']
            password = config_data['wifi']['password']
            wifi= myWiFi()
            soc = wifi.open_Socket_STA( ssid, password)  
            print('soc:', soc)
            check_for_ota_update(config_data)
            #resolve_dst_and_set_time()
            print('Current Time:', utime.localtime())
 
        led = 0
        set_State_Of_Charge(30)
        
        ip_pcWohnzimmer = "192.168.188.35"
        ip_Brauchwasser = "192.168.188.37" # Heizung tempeaturen
        evu_power         ='http://iobroker01:8087/getPlainValue/node-red.0.EVU.TotalPower'
        evu_energie       ='http://iobroker01:8087/getPlainValue/node-red.0.Haus.TotalEnergie'
        evu_ret_energie   ='http://iobroker01:8087/getPlainValue/node-red.0.EVU.EnergieReturned'
        pv_power          ='http://iobroker01:8087/getPlainValue/node-red.0.PV.Power'
        pv_energie        ='http://iobroker01:8087/getPlainValue/node-red.0.PV.TotalEnergie'
        
        
        ip_Heitzung     = '192.168.188.36' # Heizung tempeaturen
        heitzung = shelly(ip_Heitzung)
        print('-----------------starte while schleife ----------------')
        while True:
            evu_energie       ='http://iobroker01:8087/getPlainValue/node-red.0.Haus.TotalEnergie'
            iob=iobroker()
            print('evu_energie = ', iob.get_raw( evu_energie))

            
            # AF_INET - use Internet Protocol v4 addresses
            # SOCK_STREAM means that it is a TCP socket.
            # SOCK_DGRAM means that it is a UDP socket.
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.bind(('',80)) # specifies that the socket is reachable by any address the machine happens to have
            soc.listen(5)     # max of 5 socket connections
            
            # Socket accept() 
            conn, addr = soc.accept()
                        
            print("")
            print("")
            print("Got connection from %s" % str(addr))

            # Socket receive()
            request=conn.recv(1024)
            #print("")
            print("")
            print("Content %s" % str(request))

            # Socket send()
            request = str(request)
            led_on = request.find('/?LED=1')
            led_off = request.find('/?LED=0')
            ''' 
            plugstat = request.find('GET /plugstat')
            print('plugstat:' , plugstat)
            
            chargestat = request.find('GET /chargestat')
            print('chargestat:' , chargestat)
            '''
            
            if request.find('GET /plugstat') > 0:
                print('GET /plugstat')
                plugstat = get_plugstat()
                response = getRequest( plugstat )
            
            elif request.find('GET /chargestat')> 0:
                print('GET /chargestat')
                chargestat = get_chargestat()
                response = getRequest( chargestat )
            
            elif request.find('GET /setcurrent?current=')> 0:
                print('GET /setcurrent?current=')
                #TODO getValue
                current = 6.5
                set_charge_current( current)
                response = getRequest( current )

            elif request.find('GET /SoC')> 0:
                print('GET /SoC')
                response = getRequest( mySOC )
            
            elif request.find('GET /setSoC')> 0:
                print('GET /SoC')
                mySOC = get_State_Of_Charge()
                if mySOC >=100:
                    mySOC = 0
                mySOC= set_State_Of_Charge(mySOC +10)
                response = getRequest( mySOC )

            elif led_on == 6:
                print('LED ON')
                print(str(led_on))
                led = 1
                response = web_page(led)
            elif led_off == 6:
                print('LED OFF')
                print(str(led_off))
                led = 0
                response = web_page(led)
            else:
                print('get NONE')
                response = getRequest( 0 )

            conn.send('HTTP/1.1 200 OK\n')
            #conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)

            # Socket close()
            conn.close()
            soc.close()
            
            
            
