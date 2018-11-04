import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response, jsonify
import requests
import json
import bs4
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
	return getInfo(city, state)

@app.route("/getInfo/<city>--<state>", methods=["GET"])
def getInfo(city, state):
	url = "https://www.eventbrite.com/d/{}--{}/events".format(state.lower(), city.lower())
	res = requests.get(url)
	val = res.text.partition("window.__SERVER_DATA__ = ")[2].partition("</script>")[0][:-1]
	val = val[::-1].partition(";")[2][::-1]
	valz = json.loads(val)
	info_vals = []
	for val in valz["jsonld"][0]:
		try:
			event = val['url'][::-1].partition("-")[0][::-1]
			info = {'image': val['image'].replace('"', ""), "id": event, "longitude": val['location']['geo']['longitude'], "latitude": val['location']['geo']['latitude']}
			info['name'] = val['name'].replace('"', "")
			info['date'] = val["startDate"].replace('"', "")
			info_vals.append(info)
		except Exception as exp:
			print exp
	return jsonify(info_vals)

def create_new_box(page):
	box = page.select(".js-ticket-modal-btn")[0]
	print box
	newBox = str(box).replace(">Tickets", ">Full-Package Ticket (Beta)").replace("<button", '<button style="background-color:black;color:red;"').replace('js-ticket-modal-btn" ', '''js-ticket-modal-btn" onclick="location.href='https://www.google.com/';"''')
	print str(page.select(".js-ticket-modal-btn")[0]) in str(page)
	new = str(page).replace(str(page.select(".js-ticket-modal-btn")[0]), str(box) + "<br><br>" + newBox)
	return new

@app.route("/event/<idVal>", methods=["GET"])
def getPage(idVal):
	url = "https://www.eventbrite.com/e/" + idVal
	res = requests.get(url)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	page = create_new_box(page)
	return page

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
