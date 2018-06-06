import geopy.distance as gpd
import json
from datetime import datetime, timedelta, date
import pytz
from collections import defaultdict

coordinate = (47.358913,-122.086783)

locations = json.load(open('RoryJr.json'))["locations"]
pointcount = len(locations)

def dtFromMs(timestampMs):
	return datetime.fromtimestamp(timestampMs/1000.0)

times = []
locations.reverse()
for location in locations:
	if(location["accuracy"]<100):
		tempcoordinate = (location["latitudeE7"]/10**7, location["longitudeE7"]/10**7)
		if(gpd.distance(coordinate, tempcoordinate).m < 500):
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
			timeBlocks.append([timeBlock[0], timeBlock[1]])
	b = time

for block in timeBlocks:
	block[0] = dtFromMs(int(block[0]))
	block[1] = dtFromMs(int(block[1]))

sortedBlocks = defaultdict(list)

for block in timeBlocks:
	sortedBlocks[block[0].date()].append((block[0], block[1]))

final = []

for key in sortedBlocks:
	temp = sortedBlocks[key]
	timeDelta = temp[-1][1]-temp[0][0]
	timeAdditive = timedelta(microseconds = 0)
	for block in sortedBlocks[key]:
		timeAdditive += block[1]-block[0]
	print(key, ",", timeDelta, ",", timeAdditive)

