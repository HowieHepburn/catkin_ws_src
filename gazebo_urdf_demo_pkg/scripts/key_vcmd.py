#!/usr/bin/env python3
# coding=utf-8

import rospy
from geometry_msgs.msg import Twist
import curses

stdscr= curses.initscr() #初始化 curses库
curses.noecho() #关闭屏幕回显
stdscr.keypad(True)

step_vel = 0.1

vel_linear = 0.0
vel_angular = 0.0


def getvel():

    global vel_linear
    global vel_angular

    key = stdscr.getch()
    
    if key == ord('w'):
        vel_linear += step_vel
    elif key == ord('s'):
        vel_linear -= step_vel
    elif key not in [ord('w'), ord('s'), ord('a'), ord('d')]:
        if vel_linear > 0:
            vel_linear -= 0.1
            if vel_linear < 0.1:
                vel_linear = 0.0
        elif vel_linear < 0:
            vel_linear += 0.1
            if vel_linear > -0.1:
                vel_linear = 0.0
    
    if key == ord('a'):
        vel_angular += step_vel
    elif key == ord('d'):
        vel_angular -= step_vel
    elif key not in [ord('w'), ord('s'), ord('a'), ord('d')]:
        if vel_angular > 0:
            vel_angular -= 0.1
            if vel_angular < 0.1:
                vel_angular = 0.0
        elif vel_angular < 0:
            vel_angular += 0.1
            if vel_angular > -0.1:
                vel_angular = 0.0

    if key == ord(' '):
        vel_linear = 0
        vel_angular = 0

if __name__ == "__main__":
    rospy.init_node("key_vcmd")

    pub=rospy.Publisher("cmd_vel",Twist,queue_size=10)

    vel_data = Twist() # 定义速度消息

   
    while 1:
    # while not rospy.is_shutdown():
        getvel()
        vel_data.linear.x = vel_linear
        vel_data.angular.z = vel_angular
        pub.publish(vel_data)
        rospy.loginfo("car vel data publishing")
        
    curses.endwin()