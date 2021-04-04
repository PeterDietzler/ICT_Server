import ujson
import utime
from ota_update.ota_updater import OTAUpdater


def download_and_install_update_if_available(config_data):
    print('=========== download_and_install_update_if_available() ===============')
    if 'wifi' in config_data:
        ota = OTAUpdater( config_data['wifi']['gitpath'] )
        ota.install_update_if_available_after_boot( config_data['wifi']['ssid'],
                                                    config_data['wifi']['password'])
        
        #ota.download_and_install_update_if_available( config_data['wifi']['ssid'],
        #                                              config_data['wifi']['password'])
    else:
        print('No WIFI configured, skipping updates check')


def start(config_data):
    print('=========== start() ===============')
    global s
    utime.sleep_ms(10000)
    from main.ictServer import ictServer
    s = ictServer(config_data)


def boot_ict_server():
    print(' =============== boot_ict_server()  ===============')
    f = open('config.json')
    config_data = ujson.load(f)
    download_and_install_update_if_available(config_data)
    start(config_data)


s = None
boot_ict_server()
