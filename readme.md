### Web Remote

This simple webapp captures keyboard input and sends it to the robot for navigation. It also displays the latest map.
There are seperate callback functions for keyPressed and keyReleased. By default, it runs locally on port 5000.
At the moment, the buttons to start/stop navigation on the website are essentially just placeholders. They are connected to `src/app/views.py`, but don't do anything.

### Installation Instructions:
This requires some version of Python with flask and pillow installed.
```sh
sudo apt-get install python-pip
sudo pip install flask Pillow
source /home/ubuntu/catkin_ws/devel/setup.bash
rosrun web_remote run.py

```
Then, connect to http://[robot_address]:5000/ in a browser
