from config import *
import requests
import pprint

def convert(dist):
	return dist * .000621371192


athlete_info_req = requests.get(ATHLETE_URL, headers=HEADER)
athlete_info = athlete_info_req.json()

athlete_stats_req = requests.get(ATHLETE_STATS_URL, headers=HEADER)
athlete_stats = athlete_stats_req.json()

bikes = athlete_info.get('bikes')
#pprint.pprint(athlete_stats)
total = total_distance = athlete_stats.get('all_ride_totals').get('distance')
for bike in bikes:
	name = bike.get('name')
	

	if name != 'Poop Machine':
		print (name+":", "%.2f" % (bike.get('distance') * .000621371192))
		total_distance = total_distance - bike.get('distance')
print("Poop Machine: %.2f" % (total_distance * .000621371192))
print("Total mileage: %.2f" % (total * .000621371192))
