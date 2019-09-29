#!/usr/bin/env python
NO_ROBOT=True
if not NO_ROBOT:
	global rospy
	import rospy
	from std_msgs.msg import String
	from nav_msgs.msg import OccupancyGrid
	from app import robot_control
import requests, subprocess, os, math, numpy
from app import app
from PIL import Image 

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
IMG_PATH = os.path.join(DIR_PATH, "app/static/img")

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def convert_img(d):
	if d == -1:
		return 170
	if d == 0:
		return 240
	if d == 100:
		return 20
	return 0

def callback(data):
	print("start")
	'''
	This callback is called every time that a new map is available. It converts the map to JPG format.
	'''
	#convert data to readable lightness values
	imgData = [convert_img(l) for l in list(data.data)]
	#construct PIL image
	width = int(math.sqrt(len(imgData)))
	img = Image.new("L",(width,width))
	img.putdata(imgData)
	#crop + resize
	img = resize_image(img, width, 400)
	img.save(os.path.join(IMG_PATH, "map.jpg"))

def resize_image(img, width, new_width):
	'''
	takes PIL image object and returns another PIL object.
	'''
	img_pixels = img.load()
	radius = 1
	center = int(width/2)
	searching = True
	GRAY = img_pixels[0,0]
	#assuming that the maps are square
	while searching and radius < center:
		searching = False
		for w in range(center):
			i = 2*w
			region = [img_pixels[i,radius + center],
				img_pixels[i,center - radius],
				img_pixels[radius + center, i],
				img_pixels[center - radius, i]]
			if region != [GRAY] * 4:
				searching = True
				#Sin
				break
		radius += 5
	radius = radius - 2
	img = img.crop((center - radius, center - radius, center + radius, center + radius))
	ratio = new_width / width
	img = img.resize((int(width*ratio), int(width*ratio)))
	return img


def listener():
	'''
	Starts the web server and a listener for map updates.
	'''
	if NO_ROBOT:
		app.config['NO_ROBOT'] = True
	else:
		print("initializing node...")
		rospy.init_node('listener', anonymous=True)
		rospy.Subscriber("map", OccupancyGrid, callback)

		print("starting server...")
		app.config['controller'] = robot_control.turty_controller()
		app.controller['NO_ROBOT'] = False
	app.run(host='0.0.0.0', use_reloader=False)
	
def shutdownServer():
	print("shutting down server...")
	try:
		#because this isn't threaded, this request needs a timeout.
		requests.get("http://localhost:5000/shutdown", timeout=2)
	except:
		#timeout throws an exception after it expires
		pass

if __name__ == '__main__':
	if not NO_ROBOT:
		rospy.on_shutdown(shutdownServer)
	listener()
	

