import sys

import cv2
import numpy as np
import base64
from roboflow import Roboflow
import os
import shutil
import time
import serial




class RoboflowDetect:
    def __init__(self,api_key,workspace,project,base_url):
        self.serial_con = SerialCon("ttyUSB0")
        self.__marginalConfidence = 0.5
        self.__uploadFrequency = 20
        self.__lastSavedTime = time.time()
        self.__marginalXOffset = 10
        self.__marginalYOffset = 10
        
        rf = Roboflow(api_key=api_key)
        self.__version = rf.workspace(workspace).project(project).version(1)
        self.__project = rf.workspace("fyp-af9kj").project("weeds-hwlcd")
        #self.__project.image_upload_url = base_url
        #self.__version.model.base_url=base_url
        self.__video = cv2.VideoCapture(0)
        self.__ROBOFLOW_SIZE=416

    def capture(self):
        # Get the current image from the webcam
        ret, img = self.__video.read()

        # Resize (while maintaining the aspect ratio) to improve speed and save bandwidth
        height, width, channels = img.shape
        scale = self.__ROBOFLOW_SIZE / max(height, width)
        img = cv2.resize(img, (round(scale * width), round(scale * height)))
        cv2.imwrite("image.jpg",img)

    def infer(self,image):
        # Get prediction from Roboflow Infer API
        predictions= self.__version.model.predict(image)    
        return predictions
        # Parse result image
        #image = np.asarray(bytearray(resp.read()), dtype="uint8")
        #image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        #return image

    def detect(self):
        while True:
            # On "q" keypress, exit
            if(cv2.waitKey(1) == ord('q')):
                break
            
            self.capture();

            # Synchronously get a prediction from the Roboflow Infer API
            pred = self.getLoc("image.jpg")

            try:
                xLoc = pred["x"]
                yLoc = pred["y"]
                height = pred["height"]
                if(xLoc<180):
                    print("Turn left")
                    self.serial_con.sendSignal(2)
                elif(xLoc>236):
                    print("Turn right")
                    self.serial_con.sendSignal(1)
                else:
                    print("Drive forward")
                    self.serial_con.sendSignal(0)
                if(yLoc+height/2>=220):
                    print("Shredding...")
                    self.serial_con.sendSignal(3)
            except:
                print("Drive Forward",time.time())
                self.serial_con.sendSignal(0)
           
            try:
                pass
                #self.upload()
            except:
                pass
         
            #cv2.imshow('image', image)
           
        
        # Release resources when finished
        self.__video.release()
    
    def test():
        pass

    def upload(self):
        imgList = os.listdir("./data/collected")
        for image in imgList:
            self.__project.upload("./data/collected/"+image)
            os.remove("./data/collected/"+image)
    
    def saveImage(self,image):
        shutil.move(image,"./data/collected/")
        os.rename("./data/collected/image.jpg","./data/collected/"+str(round(time.time()*1000))+".jpg")

    def getLoc(self,image):
        predictions = self.infer(image)
        conf = 0
        if(len(predictions)>0):
            predictions.save(output_path="predictions.jpg",stroke=2)
            for prediction in predictions:
                if(prediction["confidence"]>conf and prediction["confidence"]>=self.__marginalConfidence):
                    #self.saveImage(image)
                    #print(prediction)
                    return prediction
        else:
            if(time.time()>self.__lastSavedTime+self.__uploadFrequency):
                #self.saveImage(image)
                self.__lastSavedTime = time.time()
        
        return {}


class SerialCon:
    def __init__(self,port):
        self.boat = serial.Serial(port=port, baudrate=9600, timeout=.1)

    def sendSignal(self,signal):
        self.boat.write(bytes(signal, 'utf-8'))