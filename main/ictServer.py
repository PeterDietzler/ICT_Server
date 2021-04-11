import utime
import os
import machine
import micropython
import builtins
import network
import socket
from main.main_website import web_page
from ota_update.ota_updater import OTAUpdater
from machine import RTC
import ntptime
import utime


def check_for_ota_update(config_data):
    print('Starte ota updater check:')
    ota = OTAUpdater( config_data['wifi']['gitpath'] )
    result = ota.check_for_update_to_install_during_next_reboot()
    #print('ota updater =', result)

def initTime():
    print('initTime()....')
    rtc = RTC()
    rtc.datetime((2017, 8, 23, 1, 12, 48, 0, 0)) # set a specific date and time
    print('Time   : ', rtc.datetime()) # get date and time

    # synchronize with ntp
    # need to be connected to wifi
    ntptime.settime() # set the rtc datetime from the remote server
    print('Time(UTC): ', rtc.datetime())    # get the date and time in UTC
    #print('rtc.now():', rtc.now())
    print('Time:', utime.gmtime())
    #print('Time:', utime.localtime())
    
def get_ntp_time():
    
    
    print('get_ntp_time().... ')
    
    year = utime.localtime()[0]       #get current year
    now=ntptime.time()
    print('getntptime() :', utime.localtime())
    HHMarch   = utime.mktime((year,3 ,(31-(int(5*year/4+4))%7),1,0,0,0,0,0)) #Time of March change to CEST
    HHOctober = utime.mktime((year,10,(31-(int(5*year/4+1))%7),1,0,0,0,0,0)) #Time of October change to CET
    
    print('HHMarch :', HHMarch)
    print('HHOctober :', HHOctober)
    print('ntptime.NTP_DELTA :', ntptime.NTP_DELTA)
    
    if now < HHMarch :               # we are before last sunday of march
        ntptime.NTP_DELTA = 3155673600-3600 # CET:  UTC+1H
        print('ntptime.NTP_DELTA before last sunday of march:', ntptime.NTP_DELTA)
    elif now < HHOctober :           # we are before last sunday of october
        ntptime.NTP_DELTA = 3155673600-7200 # CEST: UTC+2H
        print('ntptime.NTP_DELTA before last sunday of october:', ntptime.NTP_DELTA)
    else:                            # we are after last sunday of october
        ntptime.NTP_DELTA = 3155673600-3600 # CET:  UTC+1H
        print('ntptime.NTP_DELTA : after last sunday of october', ntptime.NTP_DELTA)
    
    ntptime.settime() # set the rtc datetime from the remote server


def getntptime():
    now = 0
    ntptime.host = 'nz.pool.ntp.org'
    count = 0

    print('getntptime()... ')

    while (count < 10):
        count += 1

        try:
            now = ntptime.time()
        except OSError as error:
            machine.reset()

        print('.', end = '')
        utime.sleep(1)

        if (now > 660000000):
            count = 0
            break

    if (count == 10):
        count = 0
        machine.reset()

    print(' got epoch')
    utime.sleep(1)


 #  only correct for 2021 New Zealand
    HHApril = utime.mktime((2021,4,4,3,0,0,0,0,0)) #  time of April change to NZST
    HHSept = utime.mktime((2021,9,26,2,0,0,0,0,0)) #  time of Sept change to NZDT

    if now < HHApril:               # we are before the first Sunday of April
        ntptime.NTP_DELTA = 3155673600 - (13 * 3600) #  NZDT: UTC-13H
    elif now < HHSept:              # we are before the last Sunday of Sept
        ntptime.NTP_DELTA = 3155673600 - (12 * 3600) #  NZST: UTC-12H
    else:                           # we are after the last Sunday of Sept
        ntptime.NTP_DELTA = 3155673600 - (13 * 3600) #  NZDT: UTC-13H

 #  set the time
    count = 0

    while (count < 10):
        count += 1

        my_time = ntptime.settime() # set the rtc datetime from the remote server

        print('.', end = '')
        utime.sleep(1)

        if (str(my_time) == 'None'):
            count = 0
            break

    if (count == 10):
        count = 0
        machine.reset()

    print(' time has been set')
    utime.sleep(1)
    
  
def resolve_dst_and_set_time():
    global TIMEZONE_DIFFERENCE
    global dst_on
    dst_on = 1
    TIMEZONE_DIFFERENCE = 1
    print(' resolve_dst_and_set_time()..... ')
    
    # This is most stupid thing what humans can do!
    # Rules for Finland: DST ON: March last Sunday at 03:00 + 1h, DST OFF: October last Sunday at 04:00 - 1h
    # Sets localtime to DST localtime
    '''
    if network.WLAN(network.STA_IF).config('essid') == '':
        now = mktime(localtime())
        if DEBUG_ENABLED == 1:
            print("Network down! Can not set time from NTP!")
    else:
        now = ntptime.time()
    '''
    now = ntptime.time()
    #(year, month, mdate, hour, minute, second, wday, yday) = utime.localtime(now)
    
    year = utime.localtime(now)[0]  
    if year < 2020:
        if DEBUG_ENABLED == 1:
            print("Time not set correctly!")
        return False

    dstend = utime.mktime((year, 10, (31 - (int(5 * year / 4 + 1)) % 7), 4, 0, 0, 0, 6, 0))
    dstbegin = utime.mktime((year, 3, (31 - (int(5 * year / 4 + 4)) % 7), 3, 0, 0, 0, 6, 0))

    if TIMEZONE_DIFFERENCE >= 0:
        if (now > dstbegin) and (now < dstend):
            dst_on = True
            ntptime.NTP_DELTA = 3155673600 - ((TIMEZONE_DIFFERENCE + 1) * 3600)
        else:
            dst_on = False
            ntptime.NTP_DELTA = 3155673600 - (TIMEZONE_DIFFERENCE * 3600)
    else:
        if (now > dstend) and (now < dstbegin):
            dst_on = False
            ntptime.NTP_DELTA = 3155673600 - (TIMEZONE_DIFFERENCE * 3600)
        else:
            dst_on = True
            ntptime.NTP_DELTA = 3155673600 - ((TIMEZONE_DIFFERENCE + 1) * 3600)
    if dst_on is None:
        if DEBUG_ENABLED == 1:
            print("DST calculation failed!")
            return False
    else:
        ntptime.settime()  
 

class ictServer:

    def __init__(self, config_data):
        
        print('init ictServer()')
        
        #print('Show Aktual main/.version ', self.get_version('main'))
        
        self.setAP = config_data["wifi"]["setAP"]
        print('setAP = ', self.setAP)
     
        #self.crate_Socket(config_data)
               
        self.ict_Loop_Funktion(config_data)
    
    
    def get_version(self, directory):
        print("get_version()")
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
            print('crate_Socket()', ssid, password)
            sta = network.WLAN(network.STA_IF)
            if not sta.isconnected():
                print('connecting to network...')
                sta.active(True)
                sta.connect(ssid, password)
                while not sta.isconnected():
                    pass
            print('network config:', sta.ifconfig())
            
            check_for_ota_update(config_data)
            initTime()
            getntptime()
            get_ntp_time()
            resolve_dst_and_set_time()
            print('current Time:', utime.gmtime())
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
            
