#!/usr/bin/env python3
# coding=utf-8

#动态发布

import rospy
import tf2_ros
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import TransformStamped
from turtlesim.msg import Pose


def broad_callback(pose_msg):
    broad = tf2_ros.TransformBroadcaster()
    broad_msg = TransformStamped()
    
    broad_msg.header.frame_id = "world" 
    broad_msg.header.seq = 100 
    broad_msg.header.stamp = rospy.Time.now() 
    
    broad_msg.child_frame_id = "child"

    broad_msg.transform.translation.x = pose_msg.x 
    broad_msg.transform.translation.y = pose_msg.y 
    broad_msg.transform.translation.z = 0.0
    
    qnt = quaternion_from_euler(0,0,pose_msg.theta)

    broad_msg.transform.rotation.x = qnt [0]
    broad_msg.transform.rotation.y = qnt [1]
    broad_msg.transform.rotation.z = qnt [2]
    broad_msg.transform.rotation.w = qnt [3]

    broad.sendTransform(broad_msg)
    rospy.loginfo("原xy坐标:x:%.2f,  y:%.2f\n 四元数x:%.2f ,y:%.2f z:%.2f w:%.2f",pose_msg.x,pose_msg.y,
    qnt [0],
    qnt [1],
    qnt [2],
    qnt [3],
    )

if __name__ == "__main__":
    rospy.init_node("dynamic_broad_node")
    turtle_sub = rospy.Subscriber("/turtle1/pose",Pose,broad_callback,queue_size=10)
    rospy.spin()
    # rate=rospy.Rate()
    # while not rospy.is_shutdown():
    # rate.sleep()