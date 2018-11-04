from eventbrite import Eventbrite
try:
	from keys import *
except:
	EVENTBRITE_AUTH = raw_input("EventBrite Auth: ")
	UBER_AUTH = raw_input("Uber Auth: ")


eventbrite = Eventbrite(EVENTBRITE_AUTH)


g = eventbrite.get_event("51297785056")

for val in g.keys():
	print("{} - {}".format(val, g[val]))
