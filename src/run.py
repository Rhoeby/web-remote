#!/usr/bin/env python
# JJ
#NO_ROBOT=True
NO_ROBOT=False
if not NO_ROBOT:
    global rospy
    import rospy
    from std_msgs.msg import String
    from app import robot_control
import requests, subprocess, os, math, numpy
from app import app
from PIL import Image 

# JJ
import datetime

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

def callback(data):
    print("Got explore_status message")
    print data.data
    print(datetime.datetime.now())
    if data.data == "stopped":
        print("====================================================")
        print("Robot finished exploring... browser should go to the 'Run Completed' page!")

def listener():
    # Starts the web server and a listener for updates.
    if NO_ROBOT:
        app.config['NO_ROBOT'] = True
    else:
        print("initializing node...")
        rospy.init_node('listener', anonymous=True)
        # JJ
        rospy.Subscriber("explore/explore_status", String, callback)

        print("starting server...")
        app.config['controller'] = robot_control.turty_controller()
        app.config['NO_ROBOT'] = False
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

