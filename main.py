from eventbrite import Eventbrite
import random
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

#TEST_RESP = {u'prices': [, {u'localized_display_name': u'UberXL', u'distance': 36.64, u'display_name': u'UberXL', u'product_id': u'6a99c87c-081e-432b-980b-366ba2035840', u'high_estimate': 87.0, u'low_estimate': 70.0, u'duration': 2700, u'estimate': u'$70-87', u'currency_code': u'USD'}]}
TEST_RESP = {u'localized_display_name': u'UberX', u'distance': 36.64, u'display_name': u'UberX', u'product_id': u'6a46fe24-9fbb-4ec9-a579-a0bd04d74b43', u'high_estimate': 56.0, u'low_estimate': 45.0, u'duration': 2700, u'estimate': u'$45-56', u'currency_code': u'USD'}
eventbrite = Eventbrite(EVENTBRITE_AUTH)


g = eventbrite.get_event("51297785056")

'''for val in g.keys():
	print("{} - {}".format(val, g[val]))

'''
def get_price(start_lat, start_long, end_lat, end_long):
	try:
		if len(end_long) > 25:
			end_long = '-82.30639559999997'
		if len(end_lat) > 25:
			end_lat = '34.9704971'
		params = (
	    ('start_latitude', start_lat),
	    ('start_longitude', start_long),
	    ('end_latitude', end_long),
	    ('end_longitude', end_lat),
	    ('product_id', "a1111c8c-c720-46c3-8534-2fcdd730040d"),
	    ('seat_count', 2),
		)
		response = requests.get('https://api.uber.com/v1.2/estimates/price', headers=uberHeaders, params=params)
		a = response.json()
		print a
		for val in a['prices']:
			if val['low_estimate'] == None:
				a['prices'].remove(val)
		newlist = sorted(a['prices'], key=lambda k: float(k['low_estimate']))
	except Exception as exp:
		print("ERROR ON UBER")
		print exp
		newlist = [TEST_RESP]
	try:
		newlist['lowest_estimate'] = round(random.uniform(float(newlist['lowest_estimate']),float(newlist['highest_estimate'])),2)
	except:
		pass
	return newlist[0]

if __name__ == '__main__':
	print get_price("37.775232", "-122.4197513", "37.7899886","-122.4021253")
