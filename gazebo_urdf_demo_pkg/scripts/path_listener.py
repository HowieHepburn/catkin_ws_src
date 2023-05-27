#!/usr/bin/env python3
import rospy
import numpy as np
from nav_msgs.msg import Odometry
from nav_msgs.msg import Path
from std_msgs.msg import Header
from move_base_msgs.msg import MoveBaseActionGoal
from scipy.integrate import simps

class ActualPathLengthCalculator:

    def __init__(self):
        rospy.init_node('actual_path_length_calculator', anonymous=True)
        
        # 订阅机器人位姿信息
        rospy.Subscriber('/odom', Odometry, self.odom_callback)
        # 订阅全局路径规划结果
        rospy.Subscriber('/move_base/GlobalPlanner/plan', Path, self.gpath_callback)
        # 订阅目标位置信息
        rospy.Subscriber('/move_base/goal', MoveBaseActionGoal, self.goal_callback)

        self.goal_pose = None
        self.path_length = 0.0
        self.start_time = None

        self.path = None
        
        self.flag = 0
        self.flag2 = 0
        self.goal_tolorance = 0.1
        self.positions = []

    def gpath_callback(self, msg):
        if self.flag2:
            # 计算路径规划的时间
            rospy.loginfo("Global Plan Cost time: %f s",(rospy.get_rostime() - self.start_time).to_sec())
            self.path = msg
            global_path_lenth = 0.0
            poses = [pose.pose.position for pose in self.path.poses]
            gx = [pose.x for pose in poses]
            gy = [pose.y for pose in poses]
            
            # 计算全局路径的长度
            global_path_lenth = self.calculate_path_length(gx,gy)
            
            rospy.loginfo('Global Path lenth: %f m', global_path_lenth)
            self.flag2 = 0
    
    def odom_callback(self, msg):
        # 获取机器人当前位姿
        position = msg.pose.pose.position
        self.positions.append(position)

        # if self.goal_pose is not None:
        #     rospy.loginfo("Distance %f xn:%f yn:%f xg:%f yg:%f",self.distance_2d(position, self.goal_pose),position.x,position.y,self.goal_pose.x,self.goal_pose.y)
        
        if self.goal_pose is not None:
            a = self.distance_2d(position, self.goal_pose)
            # rospy.loginfo("distance %f m", a)
        # 判断是否到达目标点
            if a <= self.goal_tolorance:
                rospy.logwarn('Reached the goal.')
                #拟合曲线
                x = [pose.x for pose in self.positions]
                y = [pose.y for pose in self.positions]

                path_length = self.calculate_path_length(x, y)
                rospy.loginfo('Cost lenth: %f m', path_length)
                rospy.loginfo("Cost time: %f s",(rospy.get_rostime() - self.start_time).to_sec())
                # 清空位置列表
                self.positions = []        
                self.flag = 0


    def goal_callback(self, msg):
        # 获取目标位置
        rospy.logwarn("Received goal position")
        
        self.goal_pose = msg.goal.target_pose.pose.position
        self.start_time = rospy.get_rostime()
        self.flag = 1
        self.flag2 = 1

    def distance_2d(self, p1, p2):
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        distance = np.sqrt(dx ** 2 + dy ** 2)
        return distance

    def calculate_path_length(self, x, y):
        # 使用 Simpson 积分计算曲线的长度
        dx = np.diff(x)
        dy = np.diff(y)
        path_length = simps(np.sqrt(dx ** 2 + dy ** 2))

        return path_length
    
if __name__ == '__main__':
    
    try:
        calculator = ActualPathLengthCalculator()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
