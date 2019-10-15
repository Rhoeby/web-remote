#!/usr/bin/env python
# JJ
NO_ROBOT=True
#NO_ROBOT=False
if not NO_ROBOT:
    global rospy
    import rospy
    from std_msgs.msg import String
    from nav_msgs.msg import OccupancyGrid
    from app import robot_control
import requests, subprocess, os, math, numpy
from app import app
from PIL import Image 

# JJ
import datetime

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

    '''
    JJ - would it be possible to resize the image first, then convert it?
    '''

    '''
    #imgData = [convert_img(l) for l in list(data.data)]
    imgData = data.data
    #construct PIL image
    # JJ
    #width = int(math.sqrt(len(imgData)))
    width = data.info.width
    
    # JJ
    print(datetime.datetime.now())

    img = Image.new("L",(width,width))
    img.putdata(imgData)
    #crop + resize
    img = resize_image(img, width, 400)

    # JJ
    img_pixels = img.load()
    for i in range(400):
      for j in range(400):
        if img_pixels[i,j] == -1:
          img_pixels[i,j] = 170
        elif img_pixels[i,j] == 0:
          img_pixels[i,j] = 240
        elif img_pixels[i,j] == 100:
          img_pixels[i,j] = 20

    img.save(os.path.join(IMG_PATH, "map.jpg"))
    '''
    '''
    img = Image.new("L",(2048,2048))
    
    img.putdata(data.data)

    img = resize_image(img, 2048, 400)
    
    img_pixels = img.load()
    for i in range(400):
      for j in range(400):
        if img_pixels[i,j] == -1:
          img.putpixel((i, j), 170)
        elif img_pixels[i,j] == 0:
          img.putpixel((i, j), 240)
        elif img_pixels[i,j] == 100:
          img.putpixel((i, j), 20)

    img.save(os.path.join(IMG_PATH, "map.jpg"))
    '''
    '''
    pixels = list(data.data)
    width = data.info.width
    
    // find the boundaries of the active data
    radius = 1
    center = int(width/2)
    searching = True
    GRAY = pixels[0]
    while searching and radius < center:
        searching = False
        for w in range(center):
            i = 2*w
            region = [pixels[i + (radius + center)*width],
                      pixels[i + (center - radius)*width],
                      pixels[radius + center + (i*width)],
                      pixels[center - radius + (i*width)]]
            if region != [GRAY] * 4:
                searching = True
                break
        radius += 5
    radius = radius - 2

    // copy the active data into the smaller image
    i = 0
    j = 0
    new_pixels = [0] * (400*400)
    for y in xrange(center - radius, center + radius):
        i = i + 1
        for x in xrange(center - radius, center + radius):
            j = j + 1
            new_pixels[i*j] = pixels[x+(y*width)]

    for i in range(400*400):
      if new_pixels[i] == -1:
        new_pixels[i] = 170
      elif new_pixels[i] == 0:
        new_pixels[i] = 240
      elif new_pixels[i] == 100:
        new_pixels[i] = 20
    '''
    
    '''
    imgData = data.data
    src_width = data.info.width
    
    img = Image.new("L", (src_width, src_width))
    
    # JJ
    print(datetime.datetime.now())
    
    img.putdata(imgData)

    # JJ - the above call takes ~180 msec!
    print(datetime.datetime.now())

    src_center = src_width/2
    dest_width = 400
    img = img.crop((src_center-(dest_width/2), src_center-(dest_width/2), src_center+(dest_width/2), src_center+(dest_width/2)))

    img.save(os.path.join(IMG_PATH, "map.jpg"))
    '''

    # JJ
    print(datetime.datetime.now())

    src_pixels = list(data.data)
    src_width = data.info.width
    src_center = src_width/2
    dest_width = 400
    dest_height = 400
    dest_pixels = [0] * (dest_width*dest_height)
    i = 0
    j = 0
    
    # JJ
    print(datetime.datetime.now())
    
    for y in xrange(src_center - dest_height/2, src_center + dest_height/2):
        for x in xrange(src_center - dest_width/2, src_center + dest_width/2):
            dest_pixels[i+(j*dest_width)] = src_pixels[x+(y*src_width)]
            i = i + 1
        j = j + 1
        i = 0
        
    # JJ
    print(datetime.datetime.now())

    img = Image.new("L", (dest_width, dest_height))
    img.putdata(dest_pixels)
    img.save(os.path.join(IMG_PATH, "map.jpg"))

    # JJ
    print(datetime.datetime.now())

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
        return self.startTime.timestamp() if self.startTime is not None else None
    def deltaTimeStamp(self):
        return self.deltaTime.total_seconds() if self.deltaTime is not None else 0

def resize_image_raw(img, width, new_width):

    img = img.crop((center - radius, center - radius, center + radius, center + radius))
    img = img.resize((400, 400))
    return img

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
    # JJ
    #img = img.resize((int(width*ratio), int(width*ratio)))
    img = img.resize((400, 400))
    return img


def listener():
    '''
    Starts the web server and a listener for map updates.
    '''
    app.config['state'] = "start"
    t = timer()
    app.config['timer'] = t
    if NO_ROBOT:
        app.config['NO_ROBOT'] = True
    else:
        print("initializing node...")
        rospy.init_node('listener', anonymous=True)
        # JJ
        #rospy.Subscriber("map", OccupancyGrid, callback)

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
    
