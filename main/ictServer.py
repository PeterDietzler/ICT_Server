import utime
import os
import machine
import micropython
import builtins



class ictServer:

    def __init__(self, config_data):
        print('Show version ', self.get_version('main'))

  
    def get_version(self, directory):
        if '.version' in os.listdir(directory):
            f = open(directory + '/.version')
            version = f.read()
            f.close()
            return version
        return '0.0'


