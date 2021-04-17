from machine import RTC
import ntptime
import utime


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
