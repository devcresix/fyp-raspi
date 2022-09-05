# Importing Libraries
import serial
import time


class Remove:
    def __init__(self,port):
        self.boat = serial.Serial(port=port, baudrate=9600, timeout=.1)

    def sendSignal(self):
        self.boat.write(bytes(3, 'utf-8'))