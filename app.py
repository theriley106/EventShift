import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
from flask import Flask, request, render_template, request, url_for, redirect, Markup, Response, send_file, send_from_directory, make_response, jsonify
import requests
import json
import re
import bs4
import main
# Flask for backend
app = Flask(__name__, static_url_path="", static_folder="static")

G = {}
@app.route('/', methods=['GET'])
def index():
	# This returns the main "index" page
	return render_template("index.html")
	# 127.0.0.1/

@app.route('/getEvents', methods=['GET', 'POST'])
def getEvents():
	location_info = request.args.get('location')
	lng = request.args.get('long')
	lat = request.args.get('lat')
	G['long'] = lng
	G['lat'] = lat
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

def create_new_box(page, idVal):
	try:
		box = page.select(".js-ticket-modal-btn")[0]
	except:
		box = ""
	print box
	newBox = str(box).replace(">Tickets", ">Full-Package Ticket (Beta)").replace("<button", '<button style="background-color:black;color:red;"').replace('js-ticket-modal-btn" ', '''js-ticket-modal-btn" onclick="location.href='/checkout/{}';"'''.format(idVal))
	#print str(page.select(".js-ticket-modal-btn")[0]) in str(page)
	try:
		new = str(page).replace(str(page.select(".js-ticket-modal-btn")[0]), str(box) + "<br><br>" + newBox.replace("js-ticket-modal-btn", ""))
	except:
		new = ""
	return new

def get_lat_long(eventID):
	info = {}
	res = requests.get("https://www.eventbrite.com/e/" + eventID)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	info['lat'] = str(page).partition('" property="event:location:longitude"')[0][::-1].partition('"')[0][::-1]
	info['lng'] = str(page).partition('" property="event:location:latitude"')[0][::-1].partition('"')[0][::-1]
	return info

@app.route("/event/<idVal>", methods=["GET"])
def getPage(idVal):
	url = "https://www.eventbrite.com/e/" + idVal
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

	res = requests.get(url, headers=headers)
	page = bs4.BeautifulSoup(res.text, 'lxml')
	try:
		G['time'] = page.select(".event-details")[0].getText().partition("Date and Time")[2].partition("Add to Calendar")[0].strip().replace("\n", " | ")
	except:
		G['time'] = None
	try:
		G['full_location'] = page.select(".event-details")[0].getText().partition("Location")[2].partition("View Map")[0].strip().replace("\n", " | ").replace("Location |", "")[2:]
		G['location'] = page.select(".event-details")[0].getText().partition("Location")[2].partition("View Map")[0].strip().replace("\n", " | ").split("|")[-1].strip()
	except Exception as exp:
		print exp
		G['full_location'] = ""
		G['location'] = ""
	try:
		G['name'] = page.select(".listing-hero-title")[0].getText()
	except:
		G['name'] = ""
	try:
		G['city'] = G['location'].partition(',')[0]
	except:
		G['city'] = ""
	try:
		G['state'] = G['location'].partition(',')[2].strip().partition(" ")[0]
	except:
		G['state'] = ""
	try:
		prices = re.findall("\d+", str(page.select(".js-display-price")[0].getText()))[0]
		G['event_price'] = int(prices)
	except:
		G['event_price'] = 35
	try:
		print str(page.select(".ico--large")[0])
		page = str(page).replace(str(page.select(".ico--large")[0]), '<img src="../logo.png">')
		page = bs4.BeautifulSoup(page, 'lxml')
	except:
		print("error on page")
	G['end_lat'] = str(page).partition('" property="event:location:longitude"')[0][::-1].partition('"')[0][::-1]
	G['end_long'] = str(page).partition('" property="event:location:latitude"')[0][::-1].partition('"')[0][::-1]
	#print("LONGS")
	#print "latitude" in str(page)
	#print str(page).partition("latitude")[2]
	#print str(page).partition('event:location:longitude" content="')[2]
	print G['end_lat']
	print G['end_long']
	page = create_new_box(page, idVal)
	return page

@app.route("/api/<event_id>")
def find_route(event_id):
	start_long = request.args.get("longitude")
	start_lat = request.args.get("latitude")
	end_vals = get_lat_long(event_id)
	end_lat = end_vals['lat']
	end_long = end_vals['lng']
	return jsonify(main.get_price(start_lat, start_long, end_lat, end_long))


@app.route("/checkout/<idVal>", methods=["GET"])
def checkout(idVal):
	try:
		print G['event_price']
	except Exception as exp:
		print("ERROR {}".format(exp))
		g = {'end_long': '34.9704971', 'city': u'Spartanburg', 'name': u'The Black Out Party', 'long': u'-82.30639559999997', 'state': u'SC', 'location': u'Spartanburg, SC 29307', 'end_lat': '-81.91012490000003', 'time': u'Fri, Nov 23, 2018, 8:00 PM \u2013 | Sat, Nov 24, 2018, 12:00 AM EST', 'lat': u'34.7189712', 'full_location': u'| Drayton Mills Marketplace | 1800 Drayton Road  | Spartanburg, SC 29307', 'event_price': 10}
	info = {}
	info['event1'] = G['event_price']
	info['sub1'] = info['event1'] + 6.25
	#info['transport'] = 11.31
	info['transport_info'] = main.get_price(G['lat'], G['long'], G['end_lat'], G['end_long'])
	info['transport'] = info['transport_info']['low_estimate']
	info['sub2'] = info['transport'] + 4.25
	info['total'] = info['sub1'] + info['transport'] + 4.25
	info['name'] = G['name']
	info['description'] = 'My Description My Description My Description My Description My Description My Description My Description My Description  My Description My Description'
	info['location'] = 'My Location'
	info['time'] = G['time']
	info['location'] = G['location']
	info['city'] = G['city']
	info['state'] = G['state']
	info['full_location'] = G['full_location']
	info['lat'] = G['lat']
	info['long'] = G['long']
	info['end_lat'] = G['end_lat']
	info['end_long'] = G['end_long']
	info['event1'] = '${:,.2f}'.format(info['event1'])
	info['sub1'] = '${:,.2f}'.format(info['sub1'])
	info['sub2'] = '${:,.2f}'.format(info['sub2'])
	info['total'] = '${:,.2f}'.format(info['total'])
	info['transport'] = '${:,.2f}'.format(info['transport'])
	print G
	return render_template("checkout.html", info=info,ride=info['transport_info'])

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
	# Example: http://127.0.0.1:5000/api/49229809686?longitude=-82.30639559999997&latitude=34.7189712
