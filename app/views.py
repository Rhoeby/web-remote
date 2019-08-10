
# A very simple Flask Hello World app for you to get started with...

from flask import render_template, send_file, request, jsonify
from app import app


@app.route('/')
def index():
	return render_template("index.html")

@app.route('/keyPressed/')
def key_pressed():
	key = request.args.get("key")
	print("KEY PRESSED: ", key)
	return jsonify({})
	

@app.route('/keyReleased/')
def key_released():
	key = request.args.get("key")
	data = request.data
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
	print("download")
	path = "static/img/text.png"
	return send_file(path)