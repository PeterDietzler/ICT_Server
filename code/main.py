import ujson
import utime
from lib.ota_update.ota_updater import OTAUpdater
from bin.ictServer import ictServer

def download_and_install_update_if_available(config_data):
    #print('==== download_and_install_update_if_available() ====')
    if 'wifi' in config_data:
        ota = OTAUpdater( config_data['wifi']['gitpath'], main_dir='bin' )
        ota.install_update_if_available_after_boot( config_data['wifi']['ssid'],
                                                    config_data['wifi']['password'])
    else:
        print('No WIFI configured, skipping updates check')


def start(config_data):
    global s
    #utime.sleep_ms(10000)
    from bin.ictServer import ictServer
    print('==== 2. start() =====')
    s = ictServer(config_data)


def boot_ict_server():
    print(' ==== 1. boot_ict_server()  ====')
    f = open('etc/UserProfile.json')
    config_data = ujson.load(f)
    download_and_install_update_if_available(config_data)
    start(config_data)


s = None
boot_ict_server()
