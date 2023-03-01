#!/usr/bin/env python

import rospy
import math
from sensor_msgs.msg import LaserScan
from race.msg import pid_input
import sys
import math
# Import whatever else you think is necessary

# Some useful variable declarations.
angle_range = 270		# sensor angle range of the lidar
car_length = 1.5	# distance (in m) that we project the car forward for correcting the error. You may want to play with this. 
desired_trajectory = 0.6	# distance from the wall (left or right - we cad define..but this is defined for right). You should try different values
vel = 5 		# this vel variable is not really used here.
error = 0.0
obstacle_check = [(80, 0.5), (90, 1.0), (100, 0.5)]

pub = rospy.Publisher('error', pid_input, queue_size=10)
# change the value of x to your team number.

##	Input: 	data: Lidar scan data
##			theta: The angle at which the distance is requried
##	OUTPUT: distance of scan at angle theta

def getRange(data,theta):
# Find the index of the arary that corresponds to angle theta.
# Return the lidar scan value at that index
# Do some error checking for NaN and ubsurd values
## Your code goes here
    if math.isnan(theta) or math.isinf(theta):
        print "encountered invalid value in getRange"
        theta = 0.0
    if theta < 0.0: theta = 0.0
    if theta > 180.0: theta = 180.0

    idx_float = ((theta+45.0) / 270.0) * (len(data.ranges) - 1)
    idx = int(round(idx_float))
    ret = data.ranges[idx]
    return ret if not math.isnan(ret) and not math.isinf(ret) else 3.0

def callback(data):
	theta = 45.0;
	a = getRange(data,theta) 
	b = getRange(data,0.0)	# Note that the 0 implies a horizontal ray..the actual angle for the LIDAR may be 30 degrees and not 0.
        c = getRange(data, 90.0)
	swing = math.radians(theta)
	
	## Your code goes here to compute alpha, AB, and CD..and finally the error.
        alpha = math.atan((a * math.cos(swing)-b) / (a * math.sin(swing)))
        dist_AB = b * math.cos(alpha)
       # distance of projection is how much the car moves in 0.1 seconds
        dist_AC = vel * 0.1
        dist_CD = dist_AB + dist_AC * math.sin(alpha)
        error = desired_trajectory - dist_CD



	## END

	msg = pid_input()
	msg.pid_error = error		
	msg.pid_vel = vel	
        msg.z = c
        if c < 0.5: msg.pid_vel = 0

	pub.publish(msg)
	

if __name__ == '__main__':
	print("Laser node started")
	rospy.init_node('dist_finder',anonymous = True)
	rospy.Subscriber("scan",LaserScan,callback)
	# subscribe to the correct /car_x/scan topic for your car..
	rospy.spin()
