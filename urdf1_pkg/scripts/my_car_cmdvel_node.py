#!/usr/bin/env python3
# coding=utf-8

import rospy
from geometry_msgs.msg import Twist
if __name__ == "__main__":
    rospy.init_node("car_vel")

    rate=rospy.Rate(10)
    pub = rospy.Publisher("cmd_vel",Twist,queue_size=10)
    while not rospy.is_shutdown():
        vel_car = Twist()
        vel_car.linear.x = 0.2
        vel_car.linear.y = 0.0
        vel_car.linear.z = 0.0

        vel_car.angular.x = 0
        vel_car.angular.y = 0
        vel_car.angular.z = 0.25

        pub.publish(vel_car)
        rospy.loginfo("car_vel pubulished")      
        rate.sleep()