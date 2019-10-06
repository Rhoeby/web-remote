import rospy
import time
from threading import Thread
from geometry_msgs.msg import Twist, Vector3
# JJ
from std_msgs.msg import Int8

class turty_controller:
    def __init__(self):
        print("turty controller init")
        self.linear_vel = Vector3(0,0,0)
        self.angular_vel = Vector3(0,0,0)
        #rospy.init_node('python_cmd_vel_talker2')
        self.publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        # JJ
        self.status = 0
        self.status_publisher = rospy.Publisher('web_remote_status', Int8, queue_size=10)
        self.status_publisher.publish(self.status)

        publishThread = Thread(target=self.talker)
        publishThread.start()
    def up(self):
        self.linear_vel.x += 0.1
    def down(self):
        self.linear_vel.x -= 0.1
    def left(self):
        self.angular_vel.z += 0.4
    def right(self):
        self.angular_vel.z -= 0.4

    # JJ
    def set_paused (self, paused):
        if paused:
            self.status = 1
        else:
            self.status = 0

    # JJ
    def get_paused (self):
        return self.status

    def talker(self):
        rate = rospy.Rate(10) # 10hz
        while not rospy.is_shutdown():
            data = Twist(self.linear_vel, self.angular_vel)
            self.publisher.publish(data)
            # JJ
            self.status_publisher.publish(self.status)

            rate.sleep()
        print("stopping publisher thread...")
