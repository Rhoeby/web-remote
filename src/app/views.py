
# A very simple Flask Hello World app for you to get started with...

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
	
@app.route('/startNavigation/')
def start_nav():
	print("START NAV")
	return jsonify({})
	
@app.route('/stopNavigation/')
def stop_nav():
	print("STOP NAV")
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
