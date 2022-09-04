from gpiozero import Motor as bldc


class BLDC:
    def __init__(self):
        self.__rightMotor = bldc(13,19)
        self.__leftMotor = bldc(12,18)

    def runForward(self,speed):
        self.__rightMotor.forward(speed=speed)
        self.__leftMotor.forward(speed=speed)

    def runBackward(self,speed):
        self.__rightMotor.backward(speed=speed)
        self.__leftMotor.backward(speed=speed)

    def turnRight(self,lSpeed,rSpeed):
        try:
            assert lSpeed>rSpeed
            self.__rightMotor.forward(speed=rSpeed)
            self.__leftMotor.forward(speed=lSpeed)
        
        except:
            pass

    def turnLeft(self,lSpeed,rSpeed):
        try:
            assert lSpeed<rSpeed
            self.__rightMotor.forward(speed=rSpeed)
            self.__leftMotor.forward(speed=lSpeed)
        
        except:
            pass