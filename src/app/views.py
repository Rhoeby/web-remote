# A very simple Flask Hello World app for you to get started with...

import subprocess, signal, os, time, json, zipfile, shutil
from moviepy.video.io.VideoFileClip import VideoFileClip

# JJ - app is run from home directory, so we need the path to be relative to that
#DATA_PATH = "app/static/data"
DATA_PATH = "catkin_ws/src/web_remote/src/app/static/data"

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
        'past_runs': [

        ]
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
        #current_app.config['explore_process'] = subprocess.Popen(["./mini_turty_explore_fast.sh", "record"], shell=False)

    return jsonify({})
    
@app.route('/pauseNavigation/')
def pause_nav():
    print("PAUSE NAV")

    # JJ
    current_app.config['controller'].set_paused(True)

    return jsonify({})

@app.route('/saveNavigation/')
def save_nav():
    location = request.args.get("location")
    print("SAVE NAV", location)
    
    # JJ 
    if not current_app.config['NO_ROBOT']:
        current_app.config['controller'].set_paused(False)
        kill_explore()

    #wait for the file to appear in the /static/temp
# JJ - app is run from home directory, so we need the path to be relative to that
#    TEMP_PATH = "app/static/temp/latestRun"
    TEMP_PATH = "catkin_ws/src/web_remote/src/app/static/temp/latestRun"
    searching = True
    timeout = 0
    while searching:
        if "video.mp4" in os.listdir(TEMP_PATH):
            '''
            JJ
            file = VideoFileClip(TEMP_PATH + "/video.mp4")
            data = {"runningTime": file.duration}
            with open(TEMP_PATH + '/info.json', 'w') as f:
                json.dump(data, f)
            
            #close moviePy file
            del file.reader
            del file
            
            #copy data to new directory
            print("Copying data...")
            shutil.copytree(TEMP_PATH, DATA_PATH + "/" + location)
            #delete files from temp folder
            for file in os.listdir(TEMP_PATH):
                os.unlink(TEMP_PATH + "/" + file)
            
            '''
            data = {"runningTime": 15.00}
            with open(TEMP_PATH + '/info.json', 'w') as f:
                json.dump(data, f)

            #copy data to new directory
            print("Copying data...")
            shutil.copytree(TEMP_PATH, DATA_PATH + "/" + location)
            #delete files from temp folder
            for file in os.listdir(TEMP_PATH):
                os.unlink(TEMP_PATH + "/" + file)

            # JJ - copy the map
            shutil.copy("catkin_ws/src/web_remote/src/app/static/img/map.jpg", DATA_PATH + "/" + location)

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
    print("DISCARD NAV")
    
    # JJ 
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
    pid = current_app.config['explore_process'].pid
    os.kill(pid, signal.SIGINT)
    if not current_app.config['explore_process'].poll():
        print ("Process correctly halted")

if __name__ == '__main__':
    raise Exception('test')
