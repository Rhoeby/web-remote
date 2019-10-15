# A very simple Flask Hello World app for you to get started with...

import subprocess, signal, os, time, json, zipfile, shutil, datetime
#from moviepy.video.io.VideoFileClip import VideoFileClip

# JJ - app is run from home directory, so we need the path to be relative to that

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(ROOT_PATH, "static")
DATA_PATH = os.path.join(ROOT_PATH, "static/data")
TEMP_PATH = os.path.join(ROOT_PATH, "static/temp")

from flask import render_template, send_file, request, jsonify, current_app, request
from app import app
    
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    # JJ
    kill_explore()

@app.route('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/wip/')
def wip():
    return render_template("wip.html")


@app.route('/keyPressed/')
def key_pressed():
    if current_app.config['NO_ROBOT']:
        return jsonify({})
    key = int(request.args.get("key"))
    print("KEY PRESSED: ", key)
    if key == 37:
        current_app.config['controller'].left()
    elif key == 38:
        current_app.config['controller'].up()
    elif key == 39:
        current_app.config['controller'].right()
    elif key == 40:
        current_app.config['controller'].down()

    return jsonify({})
    

@app.route('/keyReleased/')
def key_released():
    key = request.args.get("key")
    print("KEY RELEASED: ", key)
    return jsonify({})
    

@app.route('/loadData/')
def loadData():
    print("Page Loaded")
   
    data = {
        'battery_percentage': 88,
        'robot_name': "turty3_pro",
        'past_runs': []
    }
    for folder in os.listdir(DATA_PATH):

        path = os.path.join(DATA_PATH, folder)
        with open(os.path.join(path, "info.json")) as f:
            jsonData = json.load(f)
            data['past_runs'].append({
                "name": folder,
                "date": time.ctime(os.path.getmtime(path)),
                "length": jsonData["runningTime"],
                })
    return jsonify(data)


@app.route('/startNavigation/')
def start_nav():
    print("START NAV")
    current_app.config['state'] = "run"
    current_app.config['timer'].reset()
    current_app.config['loading'] = True

    if not current_app.config['NO_ROBOT']:
        # JJ
        if current_app.config['controller'].get_paused() == True:
            print("Robot controller was PAUSED, unpausing now")
            current_app.config['controller'].set_paused(False)
        else:
            print ("Robot controller was NOT PAUSED, starting explore_process now")
            devnull = open('/dev/null', 'w')
            #current_app.config['explore_process'] = subprocess.Popen(["./mini_turty_explore.sh"], stdout=devnull, shell=False)
            # JJ - fast - reverted
            current_app.config['explore_process'] = subprocess.Popen(["./mini_turty_explore.sh", "record"], shell=False)
            #current_app.config['explore_process'] = subprocess.Popen(["./mini_turty_explore_fast.sh", "record"], shell=False)    return jsonify({})
    return jsonify({})
@app.route('/pauseNavigation/')
def pause_nav():
    print("PAUSE NAV")
    current_app.config['timer'].pause()
    current_app.config['state'] = "pause"
    if not current_app.config['NO_ROBOT']:
        # JJ
        current_app.config['controller'].set_paused(True)

    return jsonify({})

@app.route('/resumeNavigation/')
def resume_nav():
    current_app.config['timer'].resume()
    current_app.config['state'] = "run"
    print("RESUME NAV!")
    return jsonify({})

@app.route('/navigationStatus/')
def nav_Status():
    loading_msg = "Warming up the Robot..."

    if not current_app.config['NO_ROBOT']:
        #robot control code goes here
        pass

    if current_app.config['run_ended']:
        current_app.config['state'] = "end"



    return jsonify({
        "state": current_app.config['state'],
        "loading": current_app.config['loading'],
        "run_ended": current_app.config['run_ended'],
        "loading_msg": loading_msg,
        "timerStarted": current_app.config['timer'].startTimeStamp(),
        "deltaTime": current_app.config['timer'].get_current_time(),
    })

@app.route('/saveNavigation/')
def save_nav():
    current_app.config['timer'].stop()
    current_app.config['state'] = "start"
    location = request.args.get("location")
    print("SAVE NAV", location)
    
    # JJ 
    if not current_app.config['NO_ROBOT']:
        current_app.config['controller'].set_paused(False)
        kill_explore()

    #wait for the file to appear in the /static/temp
# JJ - app is run from home directory, so we need the path to be relative to that
#    TEMP_PATH = "app/static/temp/latestRun"
    LATEST_RUN_PATH = os.path.join(TEMP_PATH, "latestRun")
    searching = True
    timeout = 0
    while searching:
        if "video.mp4" in os.listdir(LATEST_RUN_PATH):
            '''
            JJ
            file = VideoFileClip(LATEST_RUN_PATH + "/video.mp4")
            data = {"runningTime": file.duration}
            with open(LATEST_RUN_PATH + '/info.json', 'w') as f:
                json.dump(data, f)
            
            #close moviePy file
            del file.reader
            del file
            
            #copy data to new directory
            print("Copying data...")
            shutil.copytree(LATEST_RUN_PATH, DATA_PATH + "/" + location)
            #delete files from temp folder
            for file in os.listdir(LATEST_RUN_PATH):
                os.unlink(LATEST_RUN_PATH + "/" + file)
            
            '''
            data = {"runningTime": 15.00}
            with open(LATEST_RUN_PATH + '/info.json', 'w') as f:
                json.dump(data, f)

            #copy data to new directory
            print("Copying data...")
            shutil.copytree(LATEST_RUN_PATH, DATA_PATH + "/" + location)
            #delete files from temp folder
            for file in os.listdir(LATEST_RUN_PATH):
                os.unlink(LATEST_RUN_PATH + "/" + file)

            # JJ - copy the map
            shutil.copy(STATIC_PATH +  "/img/map.jpg", DATA_PATH + "/" + location)

            searching = False
        else:
            print("Waiting for video.mp4...")
            timeout = timeout + 1
            if timeout > 10:
                print("Timed out waiting for video.mp4!")
                searching = False
            time.sleep(1.0)
    print("saved Nav!")
    return jsonify({})
    
@app.route('/discardNavigation/')
def discard_nav():
    current_app.config['timer'].stop()
    print("DISCARD NAV")
    current_app.config['state'] = "start"
    
    # JJ 
    if not current_app.config['NO_ROBOT']:
        current_app.config['controller'].set_paused(False)
        kill_explore()

    return jsonify({})

@app.route('/downloadFiles/')
def downloadFiles():
    
    name = request.args.get("run")
    if name is not None:
        print("name")
        path = DATA_PATH + "/" + name 
    else:
        name = "data"
        path = DATA_PATH 
    print("DOWNLOAD", name)
    # JJ
    #shutil.make_archive("app/static/temp/data", 'zip', path)
    shutil.make_archive("catkin_ws/src/web_remote/src/app/static/temp/data", 'zip', path)

    return send_file("static/temp/data.zip", as_attachment=True, attachment_filename=name + ".zip")

@app.route("/deleteData/")
def deleteData():
    
    name = request.args.get("name")
    print("DELETE", name)
    shutil.rmtree(DATA_PATH + "/" + name)
    return jsonify({})
   

@app.route('/latestMap.jpg')
def latestMap():
    path = "static/img/map.jpg"
    return send_file(path)

# JJ
def kill_explore ():
    if not current_app.config['NO_ROBOT']:
        pid = current_app.config['explore_process'].pid
        os.kill(pid, signal.SIGINT)
        if not current_app.config['explore_process'].poll():
            print ("Process correctly halted")

if __name__ == '__main__':
    raise Exception('test')
