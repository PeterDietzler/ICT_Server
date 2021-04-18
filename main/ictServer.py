import utime
import os
import machine
import micropython
import builtins
import network
import socket
from .main_website import web_page
from ota_update.ota_updater import OTAUpdater
from machine import RTC
import ntptime
import utime

from main.get_ntp_time import resolve_dst_and_set_time
from .myWifi.myWiFi import myWiFi
from .WWW.myWiFiManager import myWiFiManager

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




	# Plugstat gibt an ob ein Stecker steckt,
	# Rückgabe ist jeweils 0 oder 1.
def get_plugstat():
    return 1

    # Chargestat gibt an, ob EVSEseitig die Ladung aktiv ist
    # Rückgabe ist jeweils 0 oder 1.
def get_chargestat():
    return 1

def get_State_Of_Charge():
    soc = 23
    return soc

def set_charge_current( current):
    print('set_charge_current():', current)
    
    
def getRequest( Value ):
    html_page = """<!DOCTYPE HTML>  
        <html>  
        <head></head>  
        <body> """ + str(Value) + """ </body>  
        </html>"""  
    return html_page




class ictServer:

    def __init__(self, config_data):
        print('init ictServer()')
        self.setAP = config_data["wifi"]["setAP"]
        print('setAP = ', self.setAP)
        #wifi = myWiFiManager()
        #wifi.init_WiFiManager()
        
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

        while True:
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
                mySOC = get_State_Of_Charge()
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
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(response)

            # Socket close()
            conn.close()
            
