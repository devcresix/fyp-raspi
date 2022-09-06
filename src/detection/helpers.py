import cv2
import numpy as np
import base64
from roboflow import Roboflow

class RoboflowDetect:
    def __init__(self,api_key,workspace,project,base_url):
        
        rf = Roboflow(api_key=api_key)
        self.version = rf.workspace(workspace).project(project).version(1)
        self.version.model.base_url=base_url
        self.video = cv2.VideoCapture(0)
        self.ROBOFLOW_SIZE=416
    
    def infer(self):
        # Get the current image from the webcam
        ret, img = self.video.read()

        # Resize (while maintaining the aspect ratio) to improve speed and save bandwidth
        height, width, channels = img.shape
        scale = self.ROBOFLOW_SIZE / max(height, width)
        img = cv2.resize(img, (round(scale * width), round(scale * height)))
        cv2.imwrite("image.jpg",img)

        # Encode image to base64 string
        retval, buffer = cv2.imencode('.jpg', img)
        img_str = base64.b64encode(buffer)

        # Get prediction from Roboflow Infer API
        prediction= self.version.model.predict("image.jpg")
        print(prediction)
        # Parse result image
        #image = np.asarray(bytearray(resp.read()), dtype="uint8")
        #image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        #return image

    def detect(self):
        while True:
            # On "q" keypress, exit
            if(cv2.waitKey(1) == ord('q')):
                break

            # Synchronously get a prediction from the Roboflow Infer API
            self.infer()
            # And display the inference results
         
            #cv2.imshow('image', image)
           
        
        # Release resources when finished
        self.video.release()
        cv2.destroyAllWindows()

