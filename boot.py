#import esp
#esp.osdebug(None)
#import gc, time
#import webrepl
#webrepl.start()
#gc.collect()

def connect_wifi_sta():
    import network
    
    # reconnect access point
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)

    # reconnect router
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connect()...')
        sta_if.active(True)
        ssid     = 'FRITZ!Box 7590 GM'
        password = '57493311541073535284'
        sta_if.connect( ssid, password)
        t0 = time
        while not sta_if.isconnected():
            #TODO Tiemeoute
            time.sleep_ms(500)
            print('.')
            pass
    else:
        print('is allredy connected')
    
    #sta_if.ifconfig(('192.168.188.76', '255.255.255.0', '192.168.188.1', '192.168.188.1'))
    print('ifconfig() -> ', sta_if.ifconfig())
   
#connect_wifi_sta()
 
 

print('END of boot.py file')