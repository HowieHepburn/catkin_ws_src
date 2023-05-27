#!/usr/bin/env python3
# coding=utf-8

import rospy
import tf2_ros
import tf
from tf2_geometry_msgs import PointStamped

if __name__ == "__main__":
    rospy.init_node("dynamic_listen_node")
    buffer = tf2_ros.Buffer()

    listener = tf2_ros.TransformListener(buffer)

    
    rate=rospy.Rate(10)
    
    while not rospy.is_shutdown():
# 动态转换组织被转换点
# 这一部分代码写在while外面就一直出问题，剪切到while里面，try前面就好了是怎么回事[发呆]
        pos = PointStamped()

        pos.header.frame_id = "child" #子坐标系
        pos.header.seq = "101"
        pos.header.stamp = rospy.Time.now()
    
        # 子坐标系读取值
        pos.point.x = 0
        pos.point.y = 0
        pos.point.z = 0

        try:
            pos_out = buffer.transform(pos, "world",rospy.Duration(1))
            rospy.loginfo("转换后坐标(2D):(%.2f %.2f %.2f) \n参考坐标系:%s",
            pos_out.point.x,
            pos_out.point.y,
            pos_out.point.z,
            pos_out.header.frame_id
            )
        except Exception as f:
            rospy.logwarn("error")
        
        rate.sleep()
        