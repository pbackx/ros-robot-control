#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import RPi.GPIO as GPIO
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

 
class MyRobot:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.stopTimer = StopTimer(self.stop, 1)
        self.left = Motor(24,25,23,0.6)
        self.right = Motor(8,7,12)

    def stop(self):
        self.left.stop()
        self.right.stop()

    def drive(self, speed, rotate):
        if rotate == 0:
            self.left.run(speed)
            self.right.run(speed)
        else:
            rotate = rotate * 0.75
            self.left.run(speed-rotate)
            self.right.run(speed+rotate)
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
