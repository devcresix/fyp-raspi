import cv2
import numpy as np
import json
import os
from threading import Thread

class Detector:
    def __init__(self):
        self.__thread = Thread(target=self.detectInVideo);
        colors = open(os.path.join(os.path.dirname(__file__),"..","..","data","colors.json"))
        colors = json.load(colors)

        self.__light_green = np.array(colors['green']['lower'])
        self.__dark_green = np.array(colors['green']['upper'])


        # Create an object to read camera video 
        self.__cap = cv2.VideoCapture(0)

        video_cod = cv2.VideoWriter_fourcc(*'XVID')
        self.__video_output= cv2.VideoWriter('captured_video.avi',
                      video_cod,
                      10,
                      (640,480))

        
    def detectInVideo(self):
        self.points=[]
        while(True):
            

            _, frame = self.__cap.read()
                        
            # Convert BGR to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        

            # Threshold the HSV image to get only blue colors
            mask = cv2.inRange(hsv, self.__light_green, self.__dark_green)

            # Bitwise-AND mask and original image
            color_mask = cv2.bitwise_and(frame,frame, mask= mask)
            
            # Write the frame into the file 'captured_video.avi'
            self.__video_output.write(color_mask)

            # Display the frame, saved in the file   
            cv2.imshow('Color Mask',color_mask)

            # convert the image to grayscale format
            img_gray = cv2.cvtColor(color_mask, cv2.COLOR_BGR2GRAY)

            # Write the frame into the file 'captured_video.avi'
            self.__video_output.write(img_gray)

            # Display the frame, saved in the file   
            cv2.imshow('Grayscale',img_gray)


            # apply binary thresholding
            ret, thresh = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY)

            # Write the frame into the file 'captured_video.avi'
            self.__video_output.write(img_gray)

            # Display the frame, saved in the file   
            cv2.imshow('Binary',thresh)

            frame_copy = frame.copy()

            # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
            contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
            for cnt in contours:
                epsilon = 0.1*cv2.arcLength(cnt,True)
                approx = cv2.approxPolyDP(cnt,epsilon,True)


                area = cv2.contourArea(approx)
                
                if area>1000:                            
                    # draw contours on the original image
                    cv2.drawContours(image=frame_copy, contours=[approx], contourIdx=-1, color=(255, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                    # compute the center of the contour
                    M = cv2.moments(cnt)
                    if M["m00"]>0:
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                        cv2.circle(frame_copy, (cX, cY), 7, (255, 255, 255), -1)
                        cv2.putText(frame_copy, "center", (cX - 20, cY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
                        self.points.append({"area":area,"point":[cX,cY]})

                        

            # Write the frame into the file 'captured_video.avi'
            self.__video_output.write(frame_copy)

            # Display the frame, saved in the file   
            cv2.imshow('Final',frame_copy)

            # Press Q on keyboard to stop recording
            if cv2.waitKey(1) & 0xFF == ord('Q'):
                self.exit()
                break

    def exit(self):
        # release video capture
        # and video write objects
        self.__cap.release()
        self.__video_output.release()

        # Closes all the frames
        cv2.destroyAllWindows() 

        print("The video was successfully saved") 
    
    def runInThread(self):
        self.__thread.start()
