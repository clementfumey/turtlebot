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
     
	# 5 HZ
        r = rospy.Rate(5);

	# create two different Twist() variables.  One for moving forward.  One for moving backward.

        # let's go forward at 0.2 m/s
        forward_cmd = Twist()
        forward_cmd.linear.x = 0.2
	# by default angular.z is 0 so setting this isn't required


        # let's go backward at 0.2 m/s
        backward_cmd = Twist()
        backward_cmd.linear.x = 0.2
	# by default angular.z is 0 so setting this isn't required


	#Go forward for 2 seconds (10 x 5 HZ) then backward  for 2 second
	count = 0
        while not rospy.is_shutdown():
	    # go forward 0.4 m (2 seconds * 0.2 m / seconds)
	    rospy.loginfo("Going Straight")
            for x in range(0,10):
                self.cmd_vel.publish(forward_cmd)
                r.sleep()
	    # turn 90 degrees
	    rospy.loginfo("Going back")
            for x in range(0,10):
                self.cmd_vel.publish(backward_cmd)
                r.sleep()            
	    count = count + 1
	    if(count == 4): 
                count = 0
	    if(count == 0): 
                rospy.loginfo("TurtleBot should be close to the original starting position (but it's probably way off)")
        
    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop Drawing Squares")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
 
if __name__ == '__main__':
    try:
        StraightLines()
    except:
        rospy.loginfo("node terminated.")
