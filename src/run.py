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
    img = Image.open(os.path.join(IMG_PATH, "map.pgm"))

    radius = 1
    center = int(img.width / 2)
    searching = True
    GRAY = img.getpixel((0,0))
    #assuming that the maps are square
    while searching and radius < center:
        searching = False
        for i in range(img.width):
            region = [img.getpixel((i,radius + center)),
                        img.getpixel((i,center - radius)),
                        img.getpixel((radius + center, i)),
                        img.getpixel((center - radius, i))]
            if region != [GRAY] * 4:
                searching = True
        radius += 1

    img = img.crop((center - radius, center - radius, center + radius, center + radius))

    #resize to width 400
    ratio = 400.0 / img.width
    img = img.resize((int(img.width*ratio), int(img.height*ratio)))
    img.save(os.path.join(IMG_PATH, "map.jpg"))



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
    
