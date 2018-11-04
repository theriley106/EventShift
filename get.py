import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')
import requests

res = requests.get("https://www.eventbrite.com/e/upstate-sc-engagement-achievement-workshops-tickets-49229809686")

with open("event.html", "w") as f:
	f.write(res.text)
