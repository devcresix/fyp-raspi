from helpers import Detector
from threading import Thread
from time import sleep

detector = Detector()

def printPoints():
    while True:
      print(detector.points)
      sleep(1000)

pointsThread =Thread(target=printPoints)


detector.runInThread()
pointsThread.start()