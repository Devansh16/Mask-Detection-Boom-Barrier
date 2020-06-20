import serial
from serial.tools import list_ports
import time
port_name = []

print('Connect Device and press c')
c = input()
if c == 'c':
    ports = list(list_ports.comports())
    for p in ports:
        port_name.append(p[0])
        
    #get a serial instance as ser and configure later
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.timeout = 1
    ser.port = port_name[0]
    
    for p in port_name:
        try:
            ser.port = p
            ser.open()
            print("connected to " + ser.port)
            break
        except:
            print(p + " Already Opend ! Retrying... ")

while True:         #Do this forever
    var = input()                                          #get input from user             
    if (var == '1'):                                                #if the value is 1         
        ser.write('1'.encode())                      #send 1 to the arduino's Data code       
        print ("LED turned ON")         
        time.sleep(1)          
    if (var == '0'): #if the value is 0         
        ser.write('0'.encode())            #send 0 to the arduino's Data code    
        print ("LED turned OFF")         
        time.sleep(1)
        