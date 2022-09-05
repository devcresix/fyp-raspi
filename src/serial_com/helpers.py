# Importing Libraries
import serial
import time


class SerialCon:
    def __init__(self,port):
        self.boat = serial.Serial(port=port, baudrate=9600, timeout=.1)

    def sendSignal(self,signal):
        self.boat.write(bytes(signal, 'utf-8'))