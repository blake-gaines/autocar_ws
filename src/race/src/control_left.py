#!/usr/bin/env python

import rospy
from race.msg import pid_input
from ackermann_msgs.msg import AckermannDriveStamped
import sys
from std_msgs.msg import Float64

# arbitrarily initialized. 25 is not a special value. This code can accept input desired velocity from the user.
angle_min_rel     = -100.0              # max left command
angle_max_rel     = 100.0               # max right command
angle_min_abs     = 0.0                 # max left VESC servo
angle_max_abs     = 1.0                 # max right VESC servo

speed_min_rel     = -100.0              # min speed command
speed_max_rel     = 100.0               # max speed command


angle_pub         = rospy.Publisher('/commands/servo/position2', Float64, queue_size = 1)
speed_pub         = rospy.Publisher('/commands/motor/duty_cycle2', Float64, queue_size = 1)

drive_pub         = rospy.Publisher('/drive', AckermannDriveStamped, queue_size=0)
# setup a publisher to publish to the /car_x/offboard/command topic for your racecar.

def output_angle_mixer(rel_angle):
    output_angle = (rel_angle - angle_min_rel)/(angle_max_rel - angle_min_rel)
    output_angle = output_angle * (angle_max_abs - angle_min_abs)
    return output_angle 

def output_speed_mixer(rel_speed):
    global duty_cycle
    if rel_speed >= 100.0: rel_speed = 100.0
    if rel_speed <= -100.0: rel_speed = -100.0
    duty_cycle = (rel_speed - 0)/(speed_max_rel - 0)
    return duty_cycle

def control(data):
    rospy.loginfo("CONTROL LEFT STARTING")
    global prev_error
    global vel_input
    global kp 
    global kd
    prev_error = 0.0
    vel_input = data.pid_vel
    theta1 = data.theta1
    theta2 = data.theta2
    kp = 20.0
    kd = 0.09
	## Your code goes here
	# 1. Scale the error 
	# 2. Apply the PID equation on error to compute steering
	# 3. Make sure the steering value is within bounds
 	
    scale_factor = 5.0
    cur_error = scale_factor * data.pid_error
    angle = (kp * cur_error + kd * (prev_error - cur_error))
    if theta1==45.0: angle = -(kp*cur_error + kd * (prev_error - cur_error))
    prev_error = cur_error
 
    if angle >= 100.0: angle = 100.0
    if angle <= -100.0: angle = -100.0

    angle_req = Float64()
    speed_req = Float64()
    angle_req.data = output_angle_mixer(angle)
    speed_req.data = output_speed_mixer(vel_input)
    angle_pub.publish(angle_req)
    speed_pub.publish(speed_req)

    ack_msg = AckermannDriveStamped()
    ack_msg.drive.speed = speed
    ack_msg.drive.steering_angle = steering_angle
    drive_pub.publish(ack_msg)
    
if __name__ == '__main__':
	global kp
	global kd
	global vel_input
	print("Listening to error for PID")
	rospy.init_node('pid_controller', anonymous=True)
	rospy.Subscriber("error2", pid_input, control)
	rospy.spin()
