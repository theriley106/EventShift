from eventbrite import Eventbrite
import requests
try:
	from keys import *
except:
	EVENTBRITE_AUTH = raw_input("EventBrite Auth: ")
	UBER_AUTH = raw_input("Uber Auth: ")

uberHeaders = {
    'Authorization': 'Token {}'.format(UBER_AUTH),
    'Accept-Language': 'en_US',
    'Content-Type': 'application/json',
}


eventbrite = Eventbrite(EVENTBRITE_AUTH)


g = eventbrite.get_event("51297785056")

'''for val in g.keys():
	print("{} - {}".format(val, g[val]))

'''
def get_price(start_lat, start_long, end_lat, end_long):
	params = (
    ('start_latitude', start_lat),
    ('start_longitude', start_long),
    ('end_latitude', end_lat),
    ('end_longitude', end_long),
    ('product_id', "a1111c8c-c720-46c3-8534-2fcdd730040d"),
    ('seat_count', 2),
	)
	response = requests.get('https://api.uber.com/v1.2/estimates/price', headers=uberHeaders, params=params)
	a = response.json()
	for val in a['prices']:
		if val['low_estimate'] == None:
			a['prices'].remove(val)
	newlist = sorted(a['prices'], key=lambda k: k['low_estimate'])
	return newlist[0]

if __name__ == '__main__':
	print get_price("37.775232", "-122.4197513", "37.7899886","-122.4021253")
