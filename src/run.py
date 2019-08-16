#!/usr/bin/env python
global rospy
import rospy, requests, subprocess, os
from std_msgs.msg import String
from nav_msgs.msg import OccupancyGrid
from app import app, robot_control
from PIL import Image 

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
IMG_PATH = os.path.join(DIR_PATH, "app/static/img")

def callback(data):
    '''
    This callback is called every time that a new map is available. It converts the map to JPG format.
    '''
    subprocess.call(["rosrun", "map_server", "map_saver"], 
        cwd= IMG_PATH, stdout=open(os.devnull, 'wb'))
    i = Image.open(os.path.join(IMG_PATH, "map.pgm"))
    i.save(os.path.join(IMG_PATH, "map.jpg"))



def listener():
    '''
    Starts the web server and a listener for map updates.
    '''
    print("initializing node...")
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("map", OccupancyGrid, callback)

    print("starting server...")
    app.config['controller'] = robot_control.turty_controller()
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
    rospy.on_shutdown(shutdownServer)
    listener()
    
