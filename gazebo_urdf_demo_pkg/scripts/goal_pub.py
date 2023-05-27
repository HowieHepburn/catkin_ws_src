#!/usr/bin/env python3

import rospy
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseActionResult
from geometry_msgs.msg import PoseStamped

class GoalPublisher:

    def __init__(self):
        rospy.init_node('goal_publisher', anonymous=True)

        # 创建发布器
        self.goal_pub = rospy.Publisher('/move_base/goal', MoveBaseActionGoal, queue_size=1)

        # 创建订阅器
        self.result_sub = rospy.Subscriber('/move_base/result', MoveBaseActionResult, self.result_callback)

        # 标志位，用于表示目标位置消息是否被接收到
        self.goal_received = False

    def result_callback(self, msg):
        # 判断接收到的消息类型，如果是目标位置消息的返回结果，则将标志位设置为True
        if msg.status.status == 3:  # 表示目标已被取消
            self.goal_received = True

    def run(self):
        # 从终端接收用户输入的目标位置信息
        x = 6.620603561401367
        y = 6.382148742675781
        z = 0.0
        orientation_x = 0.0
        orientation_y = 0.0
        orientation_z = 0.38737559739684024
        orientation_w = 0.9219219850624244

        # 创建 MoveBaseActionGoal 消息
        goal_msg = MoveBaseActionGoal()

        # 填充目标位置信息
        goal_msg.goal.target_pose.header.frame_id = 'map'
        goal_msg.goal.target_pose.pose.position.x = x
        goal_msg.goal.target_pose.pose.position.y = y
        goal_msg.goal.target_pose.pose.position.z = z
        goal_msg.goal.target_pose.pose.orientation.x = orientation_x
        goal_msg.goal.target_pose.pose.orientation.y = orientation_y
        goal_msg.goal.target_pose.pose.orientation.z = orientation_z
        goal_msg.goal.target_pose.pose.orientation.w = orientation_w

        # 发布目标位置消息
        self.goal_pub.publish(goal_msg)

        rospy.loginfo("Goal published: x={}, y={}, z={}, orientation=({}, {}, {}, {})".format(x, y, z, orientation_x, orientation_y, orientation_z, orientation_w))

        # 等待目标位置消息被接收到
        while not self.goal_received:
            rospy.sleep(0.1)

        rospy.loginfo("Goal received by move_base.")

if __name__ == '__main__':
    try:
        publisher = GoalPublisher()
        publisher.run()
    except rospy.ROSInterruptException:
        pass
