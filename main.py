from eventbrite import Eventbrite
try:
	from keys import *
except:
	EVENTBRITE_AUTH = raw_input("EventBrite Auth: ")



eventbrite = Eventbrite(EVENTBRITE_AUTH)

print eventbrite.get_user()
