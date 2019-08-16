import rospy
import time
from threading import Thread
from geometry_msgs.msg import Twist, Vector3

class turty_controller:
	def __init__(self):
		print("turty controller init")
		self.linear_vel = Vector3(0,0,0)
		self.angular_vel = Vector3(0,0,0)
		#rospy.init_node('python_cmd_vel_talker2')
		self.publisher = rospy.Publisher('cmd_vel', Twist, queue_size=10)

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


	def talker(self):
		rate = rospy.Rate(10) # 10hz
		while not rospy.is_shutdown():
			data = Twist(self.linear_vel, self.angular_vel)
			self.publisher.publish(data)
			rate.sleep()
		print("stopping publisher thread...")
