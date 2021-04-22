import requests
import ujson as json
class shelly:
    def __init__(self, ip_address, user='', password=''):
        #print('init shelly()')
        self.ip = ip_address
        self.data = 0
        self.user = user
        self.password= password
        #ip = 'http://' + self.ip + '/status'
        #print('ip=', ip)

    def read_status(self):
        ip = 'http://' + self.ip + '/status'
        #print('ip=', ip)
        r = requests.get(url = ip) # Daten abfragen
        self.data = json.loads(r.content)
        
    def get_temperature(self, channel):
        #print('get_temperature()')
        if channel>= 0 and channel <= 2:
            self.read_status()
            return self.data['ext_temperature'][str(channel)]['tC']
        else:
            print('get__temperature() channel 0,1,2 ')
            return -1
    
    def set_relay(self, state):
        if state == 1: # turn on
            #http://192.168.xxx.xxx/relay/0?turn=on
            ip = 'http://' + self.ip + '/relay/0?turn=on'
        elif state == 1: # turn off
            #http://192.168.xxx.xxx/relay/0?turn=off
            ip = 'http://' + self.ip + '/relay/0?turn=off'
        elif state == 'toggel': # turn off
            #http://192.168.xxx.xxx/relay/0?turn=toggle
            ip = 'http://' + self.ip + '/relay/0?turn=toggle'
        else:
            return -1
        requests.post(ip) # Daten abfragen
        return 0

    def get_relay(self):
        self.read_status()
        if self.data['relays']['0']['ison'] == 'false':
            return 0
        else:
            return 1
    def get_power(self, channel):
        if channel>= 0 and channel <= 2:
            self.read_status()
            return self.data['meters'][channel]['power']
        else:
            return -1

    def get_raw(self, http):
        r = requests.get(http) # Daten abfragen
        return float( r.content)

        