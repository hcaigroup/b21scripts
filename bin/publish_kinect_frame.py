#!/usr/bin/env python  
import roslib
roslib.load_manifest('b21scripts')
import rospy
import tf


if __name__ == '__main__':
    rospy.init_node('kinect_tf_broadcaster')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
    
        br.sendTransform((-4.15, 0, 0),
                         tf.transformations.quaternion_from_euler(0, 0, 0),
                         rospy.Time.now(),
                         "map",
                         "camera_base")
        br.sendTransform((-0, 0, 0),
                         tf.transformations.quaternion_from_euler(0, 0, -1.757),
                         rospy.Time.now(),
                         "camera_base",
                         "camera_depth_optical_frame")
        rate.sleep()
