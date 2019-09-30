
# A very simple Flask Hello World app for you to get started with...

import subprocess
import signal
import os

from flask import render_template, send_file, request, jsonify, current_app, request
from app import app
    
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

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
    for i in range(6):
        data['past_runs'].append({
            "name": "run" + str(i),
            "path": "/path/to/run_" + str(i),
            "date": "2019-09-0" + str(i),
            "length": "8:" + str(i) + str(i),
            })
    return jsonify(data)


@app.route('/startNavigation/')
def start_nav():
    print("START NAV")

    # JJ
    devnull = open('/dev/null', 'w')
    #current_app.config['explore_process'] = subprocess.Popen(["./mini_turty_explore.sh"], stdout=devnull, shell=False)
    current_app.config['explore_process'] = subprocess.Popen(["/home/ubuntu/mini_turty_mapping.sh"], stdout=devnull, shell=False)

    return jsonify({})
    
@app.route('/pauseNavigation/')
def pause_nav():
    print("PAUSE NAV")
    return jsonify({})

@app.route('/saveNavigation/')
def save_nav():
    location = request.args.get("location")
    print("SAVE NAV", location)

    return jsonify({})
    
@app.route('/discardNavigation/')
def discard_nav():
    print("DISCARD NAV")
    
    # JJ 
    pid = current_app.config['explore_process'].pid
    os.kill(pid, signal.SIGINT)

    if not current_app.config['explore_process'].poll():
        print "Process correctly halted"

    return jsonify({})

@app.route('/downloadFiles/')
def downloadFiles():
    path = "static/img/map.jpg"
    print("sending files from", path)
    return send_file(path)


@app.route('/latestMap.jpg')
def latestMap():
    path = "static/img/map.jpg"
    return send_file(path)


if __name__ == '__main__':
    raise Exception('test')
