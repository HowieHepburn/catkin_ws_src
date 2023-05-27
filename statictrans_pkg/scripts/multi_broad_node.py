#!/usr/bin/env python3
# coding=utf-8

import rospy
import tf2_ros
from geometry_msgs.msg import TransformStamped
from tf.transformations import quaternion_from_euler


if __name__ == "__main__":
    rospy.init_node("multi_broad_node")

    broad = tf2_ros.TransformBroadcaster()
    broad_msg_1 = TransformStamped()

    broad_msg_1.header.frame_id = "world"
    broad_msg_1.header.seq = 20
    broad_msg_1.header.stamp = rospy.Time.now()
    
    broad_msg_1.child_frame_id = "son1"
    #son1 相对于 world 的偏移量（m）




    broad_msg_1.transform.translation.x =  1
    broad_msg_1.transform.translation.y =  1
    broad_msg_1.transform.translation.z =  1

    qtn = quaternion_from_euler(0,0,0)

    broad_msg_1.transform.rotation.x = qtn[0]
    broad_msg_1.transform.rotation.y = qtn[1]
    broad_msg_1.transform.rotation.z = qtn[2]
    broad_msg_1.transform.rotation.w = qtn[3]

    rate=rospy.Rate()
    
    while not rospy.is_shutdown():
        
        rate.sleep()