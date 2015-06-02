#!/usr/bin/env python

'''
Copyright (c) 2015, Mark Silliman
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

# Written for indigo

import rospy
from geometry_msgs.msg import Twist
from math import radians

class StraightLines():
    def __init__(self):
        # initiliaze
        rospy.init_node('straightlines', anonymous=False)

        # What to do you ctrl + c    
        rospy.on_shutdown(self.shutdown)
        
        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
     
	# 10 HZ
        r = rospy.Rate(10);

	# create two different Twist() variables.  One for moving forward.  One for moving backward.

        # let's go forward at 0.1 m/s
        forward_cmd1 = Twist()
        forward_cmd1.linear.x = 0
	# by default angular.z is 0 so setting this isn't required
	
        # let's go backward at 0.1 m/s
        backward_cmd1 = Twist()
        backward_cmd1.linear.x = 0
	# by default angular.z is 0 so setting this isn't required


	#Go forward for 2 seconds (10 x 10 HZ) then backward  for 2 second
	count = 0
        while not rospy.is_shutdown():
	    
	    rospy.loginfo("Going Straight")
	    # go forward 3 m (2 seconds * 0.7 m / seconds)
	        for x in range(0,50):
                self.cmd_vel.publish(forward_cmd1)
                forward_cmd1.linear.x += 0.1
                r.sleep()
                
             for x in range(0,50):
                self.cmd_vel.publish(forward_cmd1)
                r.sleep()   
                
            for x in range(0,50):
                self.cmd_vel.publish(forward_cmd1)
                forward_cmd1.linear.x -= 0.1
                r.sleep()

                
	    
	    rospy.loginfo("Going back")
	        for x in range(0,50):
                self.cmd_vel.publish(backward_cmd1)
                backward_cmd1.linear.x -= 0.1
                r.sleep()
                
             for x in range(0,50):
                self.cmd_vel.publish(backward_cmd1)
                r.sleep()   
                
            for x in range(0,50):
                self.cmd_vel.publish(backward_cmd1)
                backward_cmd1.linear.x += 0.1
                r.sleep()
                
                          
	    count = count + 1
	    if(count == 4): 
                count = 0
	    if(count == 0): 
                rospy.loginfo("TurtleBot should be close to the original starting position (but it's probably way off)")
        
    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop Lines")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
 
if __name__ == '__main__':
    try:
        StraightLines()
    except:
        rospy.loginfo("node terminated.")
