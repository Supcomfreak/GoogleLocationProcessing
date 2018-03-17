import geopy.distance as gpd
import json
from datetime import datetime, timedelta, date
import pytz


coordinate = (47.651295,-122.0311216)

locations = json.load(open('LocationHistory.json'))["locations"]
pointcount = len(locations)

def dtFromMs(timestampMs):
	return datetime.fromtimestamp(timestampMs/1000.0)

times = []
locations.reverse()
for location in locations:
	if(location["accuracy"]<100):
		tempcoordinate = (location["latitudeE7"]/10**7, location["longitudeE7"]/10**7)
		if(gpd.distance(coordinate, tempcoordinate).m < 200):
			times.append(location["timestampMs"])
		else:
			times.append("break")

timeBlocks = []
timeBlock = [0, 0]
b = "break"
for time in times:
	if(time != b):
		if(b == "break"):
			timeBlock[0] = time		
		if(time == "break"):
			timeBlock[1] = b
			timeBlocks.append((timeBlock[0], timeBlock[1]))
	b = time

for block in timeBlocks:
	block = (dtFromMs(int(block[0])), dtFromMs(int(block[1])))

start = []
end = []
a = datetime.min
"""
for block in timeBlocks:
	if(len(timeBlocks) == 0):
		break
	
	if(block[0].date() != a.date()):
		if(len(start)>0):
			end.append(b)
		start.append(block[0])
	b = block[1]

workdays = zip(start, end) 
"""
for block in timeBlocks:
	if(((int(block[1])-int(block[0]))/3600000)>0.01):
		print(dtFromMs(int(block[0])), ", ", dtFromMs(int(block[1])), ", ", (int(block[1])-int(block[0]))/3600000)
