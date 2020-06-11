#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import RPi.GPIO as GPIO
import serial
from threading import Timer

class StopTimer:
    def __init__(self, stopCallback, delay=0.3):
        self.delay=delay
        self.timer=None
        self.stopCallback=stopCallback

    def reset(self):
        if self.timer is not None:
            self.timer.cancel()

        self.timer = Timer(self.delay, self.stopCallback)
        self.timer.start()

class Motor:
    def __init__(self, in1, in2, en, multiplier=1):
        self.in1 = in1
        self.in2 = in2
        self.en = en
        self.multiplier = multiplier
        GPIO.setup(self.in1,GPIO.OUT)
        GPIO.setup(self.in2,GPIO.OUT)
        GPIO.setup(self.en,GPIO.OUT)
        GPIO.output(self.in1,GPIO.LOW)
        GPIO.output(self.in2,GPIO.LOW)
        self.pwm=GPIO.PWM(self.en,1000)
        self.pwm.start(50)

    def stop(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)

    def run(self, speed):
        if speed == 0:
            self.stop()
        else:
            pwmSpeed=min(abs(speed),1.0)*100*self.multiplier
            rospy.loginfo(rospy.get_caller_id() + " pwm: " + str(pwmSpeed))
            self.pwm.ChangeDutyCycle(pwmSpeed)
            if speed > 0:
                GPIO.output(self.in1,GPIO.HIGH)
                GPIO.output(self.in2,GPIO.LOW)
            elif speed < 0:
                GPIO.output(self.in1,GPIO.LOW)
                GPIO.output(self.in2,GPIO.HIGH)

class Sabertooth:
    def __init__(self, serial_port='/dev/ttyS0', baudrate=9600, max_throttle=64):
        self.serial = serial.Serial(serial_port, baudrate)
        self.max_throttle = max_throttle

    def stop(self):
        self.serial.write([64, 192])

    def drive(self, left, right):
        left = max(min(left, 1.0),-1.0)
        right = max(min(right, 1.0),-1.0)
        left_int = 64+int(round(self.max_throttle*left))
        right_int = 192+int(round(self.max_throttle*right))
        command = bytearray([left_int, right_int])
        rospy.loginfo(rospy.get_caller_id() + " sending command to Sabertooth: " + str(list(command)))
        self.serial.write(command)


class MyRobot:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.stopTimer = StopTimer(self.stop, 1)
        self.sabertooth = Sabertooth(max_throttle=48)

    def stop(self):
        self.sabertooth.stop()

    def drive(self, speed, rotate):
        # sp = 1 + r = 0 -> both forward
        # sp = -1 + r = 0 -> beide achteruit
        # sp = 0 + r = 1 -> rechts vooruit, links achteruit
        # sp = 0 + r = -1 -> rechts achteruit, links vooruit
        # sp = 1 + r = 1 -> rechts vooruit, links stil

        left = (speed + rotate) / 2
        right = (speed - rotate) /2
        self.sabertooth.drive(left, right)
        self.stopTimer.reset()

myRobot = MyRobot()

def callback(twist):
    forward = twist.linear.x
    rotate = twist.angular.z
    rospy.loginfo(rospy.get_caller_id() + " forward: " + str(forward) + " rotation: " + str(rotate))
    myRobot.drive(forward,rotate)
    
def listener():
    rospy.init_node('cmd_vel_listener', anonymous=True)
    rospy.Subscriber("cmd_vel", Twist, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
