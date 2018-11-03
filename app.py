from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response, jsonify
import requests
import json
# Flask for backend
app = Flask(__name__, static_url_path="", static_folder="static")


@app.route('/', methods=['GET'])
def index():
	# This returns the main "index" page
	return render_template("index.html")
	# 127.0.0.1/

@app.route('/getEvents', methods=['GET', 'POST'])
def getEvents():
	location_info = request.args.get('location')
	address = location_info.split(", ")
	state = address[-2]
	city = address[-3]
	print state
	print city
	return ""

@app.route("/getInfo/<city>--<state>", methods=["GET"])
def getInfo(city, state):
	url = "https://www.eventbrite.com/d/{}--{}/events".format(state.lower(), city.lower())
	res = requests.get(url)
	val = res.text.partition("window.__SERVER_DATA__ = ")[2].partition("</script>")[0][:-1]
	val = val[::-1].partition(";")[2][::-1]
	val = json.loads(val)
	val = val["jsonld"][0][0]
	event = val['url'][::-1].partition("-")[0][::-1]
	info = {"id": event, "longitude": val['location']['geo']['longitude'], "latitude": val['location']['geo']['latitude']}
	return jsonify(info)


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
