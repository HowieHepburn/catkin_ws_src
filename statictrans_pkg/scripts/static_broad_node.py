#!/usr/bin/env python3
# coding=utf-8

import rospy
import tf2_ros
from tf.transformations import quaternion_from_euler 
from geometry_msgs.msg import TransformStamped


# 节点：坐标转换发布函数
# 作用：发布子坐标系相对父坐标系的偏移关系，数据类型为TransformStamped
# rosmsg info geometry_msgs/TransformStamped 
# std_msgs/Header header
#   uint32 seq
#   time stamp
#   string frame_id
# string child_frame_id            #子坐标系的frame_id
# geometry_msgs/Transform transform
#   geometry_msgs/Vector3 translation
#     float64 x
#     float64 y
#     float64 z
#   geometry_msgs/Quaternion rotation
#     float64 x
#     float64 y
#     float64 z
#     float64 w

if __name__ == "__main__":
    rospy.init_node("static_broad_node")

    broad = tf2_ros.StaticTransformBroadcaster()   #坐标变换专用数据发送函数
    
    broad_msg = TransformStamped()

    broad_msg.header.frame_id = "world"  #父坐标系
    broad_msg.header.stamp = rospy.Time.now()  #时间戳
    broad_msg.header.seq = 20  #序列号

    broad_msg.child_frame_id = "laser" #子坐标系

    # 子坐标系相对于父坐标系的偏移量
    broad_msg.transform.translation.x = 2.0 
    broad_msg.transform.translation.y = 0.0
    broad_msg.transform.translation.z = 0.5 

    # 四元数 从欧拉角转换，然后设置四元数
    qtn = quaternion_from_euler(0,0,0)
    broad_msg.transform.rotation.x = qtn[0]
    broad_msg.transform.rotation.y = qtn[1]
    broad_msg.transform.rotation.z = qtn[2]
    broad_msg.transform.rotation.w = qtn[3]

    # rate=rospy.Rate(1)
    
    # while not rospy.is_shutdown():
    broad.sendTransform(broad_msg)
    rospy.spin()
    # rate.sleep()