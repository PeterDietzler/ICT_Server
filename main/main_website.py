# ************************
# https://techtotinker.blogspot.com/2020/11/016-esp32-micropython-web-server-esp32.html?m=1
#
import machine
import time
import esp32

led = machine.Pin(2,machine.Pin.OUT)
led.off()


# ************************
# Function for creating the
# web page to be displayed
def web_page(myled):
    
    
    
    espHall = esp32.hall_sensor()     # read the internal hall sensor
    #espTemperatur = esp32.raw_temperature() # read the internal temperature of the MCU, in Farenheit
    espTemperatur = (esp32.raw_temperature() - 32) * 5/9
    
    
    if myled==1:
        led.value(1)
        led_state = 'ON'
        print('led is ON')
        R1= 28010
        R2= 28020
        R3= 28030
        R4= 28040
        R5= 28050
        R6= 28060
        R7= 28070
        R8= 28080
 
    elif myled==0:
        led_state = 'OFF'
        led.value(0)
        print('led is OFF')
        R1= 2801
        R2= 2802
        R3= 2803
        R4= 2804
        R5= 2805
        R6= 2806
        R7= 2807
        R8= 2808
    
    
    html_page = """<!DOCTYPE HTML>  
        <html>  
        <head>  
          <meta name="viewport" content="width=device-width, initial-scale=1">  
        </head>  
        <body>  
           <center><h2> """ + 'ESP32' +     """ </h2></center>  
           <center><p>Projekt: python-beispiele/microPython/HalloWelt </p></center> 
           <center><p>Hall       : """ + str(espHall) +     """ mT </p></center> 
           <center><p>Temperatur : """ + str(espTemperatur) + """ °C</p></center> 
           <center>  
             <form>  
               <button type='submit' name="LED" value='1'> LED ON </button>  
               <button type='submit' name="LED" value='0'> LED OFF </button>  
             </form>  
           </center>  
           <center><p> <strong> Sinus </strong></p></center>  
           <center><p>R1 = <strong>""" + str(R1) + """</strong> R3 = <strong>""" + str(R3) + """</strong></p></center>  
           <center><p>R2 = <strong>""" + str(R2) + """</strong> R4 = <strong>""" + str(R4) + """</strong></p></center>  
           <center><p> <strong> Cosinus </strong></p></center>  
           <center><p>R5 = <strong>""" + str(R5) + """</strong> R7 = <strong>""" + str(R7) + """</strong></p></center>  
           <center><p>R6 = <strong>""" + str(R6) + """</strong> R8 = <strong>""" + str(R8) + """</strong></p></center>  
        </body>  
        </html>"""  
    return html_page



    
