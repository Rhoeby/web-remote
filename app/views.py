
# A very simple Flask Hello World app for you to get started with...

from flask import render_template, request, jsonify
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
	