#!/usr/bin/env python

import rospy
from race.msg import drive_values
from race.msg import drive_param
from std_msgs.msg import Bool


"""
What you should do:
 1. Subscribe to the keyboard messages (If you use the default keyboard.py, you must subcribe to "drive_paramters" which is publishing messages of "drive_param")
 2. Map the incoming values to the needed PWM values
 3. Publish the calculated PWM values on topic "drive_pwm" using custom message drive_values
"""

def convert(val):
    return int(9831 + 32.7 * val)

def callback(data):
    print 'received data: %f, %f' % (data.velocity, data.angle)
    msg_to_send = drive_values()
    msg_to_send.pwm_drive = convert(data.velocity)
    msg_to_send.pwm_angle = convert(data.angle)
    # print 'send: %d, %d' % (msg_to_send.pwm_drive, msg_to_send.pwm_angle)
    pub.publish(msg_to_send)

if __name__ == '__main__':
    global pub
    rospy.init_node('talker')
    rospy.Subscriber('drive_parameters', drive_param, callback)
    pub = rospy.Publisher('drive_pwm', drive_values, queue_size=10)
    print 'Serial talker initialized'
    rospy.spin()
