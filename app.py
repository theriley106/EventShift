from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response, jsonify
# Flask for backend
try:
	from keys import *
except:
	EVENTBRITE_AUTH = raw_input("EventBrite Auth: ")


app = Flask(__name__, static_url_path="", static_folder="static")


@app.route('/', methods=['GET'])
def index():
	# This returns the main "index" page
	return render_template("index.html")
	# 127.0.0.1/

if __name__ == "__main__":
	app.run(host='0.0.0.0')
