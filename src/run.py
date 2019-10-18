#!/usr/bin/env python
# JJ
#NO_ROBOT=True
NO_ROBOT=False
import datetime
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
    # JJ - minimal useful print
    print("Got explore_status message: " + data.data)
    #print(datetime.datetime.now())
    if data.data == "stopped":
        #if the robot is running and stops on its own
        if app.config['state'] == "run":
            app.config['state'] = "end"

        #if the robot was manually stopped
        if app.config['state'] == "pause":
            app.config['state'] = "start"

        # JJ - discard nav scenario (from either browser-invoked "End" or robot-invoked "stopped")
        #if app.config['state'] == "start" and app.config["loading"]:
        app.config['loading'] = False

    if data.data == "exploring" and app.config["loading"]:
        if app.config['state'] != "pause":
            app.config['loading'] = False
            app.config['timer'].reset()

class timer:
    def __init__(self):
        self.startTime = None
        self.deltaTime = datetime.timedelta(0)
    def reset(self):
        self.startTime = datetime.datetime.now()
        self.deltaTime = datetime.timedelta(0)


    def pause(self):
        if self.startTime is None:
            return
        self.deltaTime = self.deltaTime + datetime.datetime.now() - self.startTime
        self.startTime = None
    def resume(self):
        if self.startTime != None:
            raise Exception("bad state")
        self.startTime = datetime.datetime.now()
    def stop(self):
        self.startTime = None
        self.deltaTime = datetime.timedelta(0)
    def get_current_time(self):
        if self.startTime is None:
            temptime = self.deltaTime
        else:
            temptime = self.deltaTime + datetime.datetime.now() - self.startTime
        return temptime.total_seconds()
        
    def startTimeStamp(self):
        return (self.startTime-datetime.datetime(1970,1,1)).total_seconds() if self.startTime is not None else None
    def deltaTimeStamp(self):
        return self.deltaTime.total_seconds() if self.deltaTime is not None else 0

def listener():
    # Starts the web server and a listener for updates.
    app.config['state'] = "start"
    app.config['timer'] = timer()
    app.config['loading'] = False
    app.config['run_ended'] = False
    # JJ - anti-spew
    app.config['prev_state'] = app.config['state']

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
