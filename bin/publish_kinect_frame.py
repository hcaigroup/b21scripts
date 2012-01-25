#!/usr/bin/env python
import roslib
roslib.load_manifest('b21scripts')
import rospy
import tf
from tf import TransformListener
import geometry_msgs.msg

if __name__ == '__main__':
    rospy.init_node('kinect_tf_broadcaster')
    br = tf.TransformBroadcaster()
    tf_listener = tf.TransformListener()
    pub = rospy.Publisher("/Human/Pose", geometry_msgs.msg.PoseStamped)
    humanpose = geometry_msgs.msg.PoseStamped()

    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        now = rospy.Time.now()
        br.sendTransform((0, 4.15, -0.92),
                         tf.transformations.quaternion_from_euler(0, 0, -1.57079633),
                         now,
                         "map",
                         "camera_depth_optical_frame")

        rate.sleep()

        try:
            tf_listener.waitForTransform("map", "neck_1", now - rospy.Duration(0.1), rospy.Duration(0.2))
            ((x,y,z), (ox, oy, oz, ow)) = tf_listener.lookupTransform("/map", "/neck_1", now)

            # TODO: Need to do sensor fusion from multiple kinects to get human pose for multiple humans (navigation ROS interface can only handle 1 human for now)

            humanpose.pose.position.x = x
            humanpose.pose.position.y = y
            humanpose.pose.orientation.x = ox
            humanpose.pose.orientation.y = oy
            humanpose.pose.orientation.z = oz
            humanpose.pose.orientation.w = ow

            pub.publish(humanpose)

        except tf.LookupException, e:
            rospy.logerr("LookupException: tf lookup failed from %s to %s: %s", "map", "neck_1", e)
        except tf.ExtrapolationException, e:
            rospy.logerr("ExtrapolationException: tf lookup failed from %s to %s: %s", "map", "neck_1", e)
        except tf.Exception, e:
            rospy.logerr("tf lookup failed from %s to %s: %s", "map", "neck_1", e)
