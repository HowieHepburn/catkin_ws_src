#!/usr/bin/env python3
# coding=utf-8
# 静态坐标系订阅

import rospy
import tf2_ros
import tf
# from tf2_geometrymsgs.geometry_msgs.msg import PointStamped
from tf2_geometry_msgs import PointStamped  # 必须导入此消息类型


if __name__ == "__main__":
    rospy.init_node("static_listen_node")
    
    buffer = tf2_ros.Buffer()
    sub = tf2_ros.TransformListener(buffer)
    
    ts = PointStamped()

    ts.header.seq = 21
    ts.header.frame_id = "world"  #父坐标系
    ts.header.stamp = rospy.Time.now()

    #子坐标系下的坐标值
    ts.point.x = 0.3
    ts.point.y = 0.2
    ts.point.z = 1.0

    rate = rospy.Rate(10)
    
    while not rospy.is_shutdown():
        try:
            ts_out = buffer.transform(ts, "world")

            rospy.loginfo("转换后坐标:%.2f , %.2f ,%.2f,参考坐标系：%s",
                                                                        ts_out.point.x,
                                                                        ts_out.point.y,
                                                                        ts_out.point.z,
                                                                        ts_out.header.frame_id)
        except Exception as e:
            rospy.logwarn("error")

        rate.sleep()