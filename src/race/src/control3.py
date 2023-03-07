#!/usr/bin/env python

import rospy
from race.msg import pid_input
from ackermann_msgs.msg import AckermannDrive
import sys
sys.path.append('/home/jiangwei/.local/lib/python3.6/site-packages/cvxopt')
import cvxopt
from std_msgs.msg import Float64
from cvxopt import matrix, solvers
import math
import numpy as np

# arbitrarily initialized. 25 is not a special value. This code can accept input desired velocity from the user.
angle_min_rel     = -100.0              # max left command
angle_max_rel     = 100.0               # max right command
angle_min_abs     = 0.0                 # max left VESC servo
angle_max_abs     = 1.0                 # max right VESC servo

speed_min_rel     = -100.0              # min speed command
speed_max_rel     = 10.0               # max speed command

speed_req = Float64()
angle_pub         = rospy.Publisher('/commands/servo/position', Float64, queue_size = 1)
speed_pub         = rospy.Publisher('/commands/motor/duty_cycle', Float64, queue_size = 1)

# setup a publisher to publish to the /car_x/offboard/command topic for your racecar.

vd = 2       # Desired velocity of ego vehicle (m/s)
v = 2        # Initial velocity of ego vehicle (m/s)
v0 = 3.0       # Front vehicle velocity (m/s)
z = 10.0      # Initial Distance between front vehicle and ego vehicle (m)
dt = 0.01       # Value of time step (s)

m = 3.0      # mass of ego vehicle (kg)
ca = 2        # max acceleration ca*g
cd = 2          # max deacceleration -cd*g
g = 9.81        # gravitational acceleration

fsilon = 5.0    # coeff to Exponential CLF
gamma = 1.0     # Coeff to exponential CBF
x0 = 0.5        # Stopping distance from front vehicle
    
f0 = 0.1        # Coeff for aerodynamic drag
f1 = 5.0
f2 = 0.25

A = 10.0        # Front vehicle velocity amplitude
f = 0.1           # Front vehicle velocity frequency


class Controller:
    def __init__(self):
        self.internal_vel = v
        self.x2 = v
        self.z = z
        self.u = 0
        self.u_old = 5
        self.t = 0
        self.v0 = v0
 
    def FR(self):
        '''
        aerodynamic drag force for given ego vehicle velocity(x2)
        '''
        x2 = self.x2
        Fr = f0 + f1*x2 + f2*(x2**2)
        return Fr


    def Si_0(self):
        '''
        calculation of si0 for Lyapunov Constraints
        '''
        x2 = self.x2
        Fr = self.FR()
        si0 = -2.0*((x2 - vd)*Fr/m) + fsilon*((x2-vd)**2)
        return si0

    def Si_1(self):
        '''
        calculation of si1 for Lyapunov Constraints
        '''
        x2 = self.x2
        si1 = 2.0*(x2 - vd)/m
        return si1

    def H(self):
        '''
        calculation of h for barrier function
        '''
        x2 = self.x2
        z = self.z
        h = z - 1.8*x2 - x0 -(0.5*((self.v0-x2)**2))/(cd*g)
        return h


    def B(self):
        '''
        calculation of barrier function
        '''
        x2 = self.x2
        z = self.z
        h = self.H()
        b = -math.log(h/(1.0+h))
        return b


    def LFB (self):
        '''
        calculation of LFB for CBF Constraints
        '''
        x2 = self.x2
        z = self.z
        Fr = self.FR()
        h = self.H()
        Lfb = -(-Fr*(self.v0-x2)/(cd*g*m) + 1.8*Fr/m + self.v0 - x2)/(h*(1.0+h))
        return Lfb


    def LGB(self):
        '''
        calculation of LGB for CBF Constraints
        '''
        x2 = self.x2
        z = self.z
        h = self.H()
        Lgb = (1.8 - (self.v0-x2)/(cd*g))/(m*h*(1.0+h))
        return Lgb



    def PSC(self):
        '''
        penality for softness in Lyapunov constraints
        '''
        x2 = self.x2
        z = self.z
        b = self.B()
        psc = math.exp((gamma/(10.0*b))-3)
        return psc


    def fdbk_callback(self, data):
        '''
        feedback callback to get current state
        data type is fdbk_type where
        data.fdbk_type = [x2, z, u_old, v0]
        '''
        global prev_error
        global vel_input
        global kp 
        global kd
        prev_error = 0.0
        vel_input = data.pid_vel
        self.x2 = data.realvel
        self.z = data.z
        self.v0 = v0
        kp = 14.0
        kd = 0.09
        ## Your code goes here
        # 1. Scale the error 
        # 2. Apply the PID equation on error to compute steering
        # 3. Make sure the steering value is within bounds

        scale_factor = 5.0
        cur_error = scale_factor * data.pid_error
        angle = -(kp * cur_error + kd * (prev_error - cur_error))
        prev_error = cur_error


        angle_req = Float64()
        speed_req = Float64()
        angle_req.data = output_angle_mixer(angle)
        
        angle_pub.publish(angle_req)
        




    def update_time(self):
        self.t += dt

    def solution(self):
        '''
        solve the input(acceleration) for safety aware ACC using CLF
        and CBL concept
        This function will generate input for speed(x2) and current distance
        between ego vehicle and front vehicle
        '''
        # self.update_time()
        # self.get_velocity()  #Uncomment this to use either 'linear or sinusoidal front vehicle velocity profile. The default front vehicle velocity is obtained through vicon_bridge' ros package.
        b = self.B() # Calculates Barrier Function 
        psc = self.PSC() # Penalty for softness in Lyapunov Constraints
        Fr = self.FR() # aerodynamic drag force for given ego vehicle velocity(x2)

        Aclf = self.Si_1()         # control Lyapunov constraint
        bclf = -self.Si_0()  

        Acbf = self.LGB()       # control barrier constraint
        bcbf = -self.LFB() + (gamma/b)


        '''
        formulation for CVXOPT
            min u'*Q*u + p*u
            subject to 
                G*u <= h
        '''
        Q = 2.0*matrix([[1/m**2, 0.0], [0.0, psc]])
        p = -2.0*matrix([Fr/(m**2), 0.0])
        G = matrix([[Aclf, Acbf] ,[-1.0, 0.0]])
        h = matrix([bclf, bcbf])

        solvers.options['show_progress'] = False
        sol = solvers.qp(Q, p, G, h)

        U = sol['x']
        self.u = U[0]/m

def Solve():
    '''
    initialization of controller 
    default state:
    velocity = 20, distence = 100
    '''
    controller = Controller()

    '''
    subscribe to acc/feedback topic to get current state
    
    '''
    rospy.init_node('acc_controller')       #initialize acc_controller node
    rospy.Subscriber("error", pid_input, controller.fdbk_callback)

    
    rate = rospy.Rate(40)                  #node frequency 40hz
    while not rospy.is_shutdown():

        try:            # create exception to get rid of python float round off
            controller.solution()
          

        except:
            controller.u = controller.u_old

        
        vel = controller.x2+dt*controller.u  # Computation of velocity given by: v = u+a*t
      

      	# Compute Internal velocity of ego vehicle and to overcome actuator saturation limits
        controller.internal_vel = controller.internal_vel + dt*controller.u
        if abs(controller.internal_vel - vel) > 0.1:
            controller.internal_vel = vel
            speed_req.data = output_speed_mixer(controller.internal_vel)

 		# Velocity input to the TurtleBot
        speed_pub.publish(speed_req)  


        rate.sleep()

        
def output_angle_mixer(rel_angle):
    if rel_angle >= 100.0: rel_angle = 100.0
    if rel_angle <= -100.0: rel_angle = -100.0

    output_angle = (rel_angle - angle_min_rel)/(angle_max_rel - angle_min_rel)
    output_angle = output_angle * (angle_max_abs - angle_min_abs)
    return output_angle 

def output_speed_mixer(rel_speed):
    global duty_cycle
    if rel_speed >= 100.0: rel_speed = 100.0
    if rel_speed <= -100.0: rel_speed = -100.0
    duty_cycle = (rel_speed - 0)/(speed_max_rel - 0)
    if duty_cycle <=0.0: duty_cycle = 0.0
    return duty_cycle


    
if __name__ == '__main__':
	Solve()

