import re
data = []

Y = int(input()) * 2

def dist(x1, y1, x2, y2):
	return abs(x2 - x1) + abs(y2 - y1)

beacons = set()
while True:
	l = input().strip()
	if l == "":
		break
	match = re.match(r"Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)", l)
	if match:
		x1, y1, x2, y2 = tuple(map(int, match.groups()))
		data.append((x1, y1, x2, y2, dist(x1, y1, x2, y2)))
		beacons.add((x2, y2))
	else:
		raise Exception(l)

#print(data)

for y in range(0, Y + 1):
	hits = []
	for x1, y1, x2, y2, d in data:
		w = d - abs(y1 - y)
		if w > 0:
			hits.append([x1 - w, x1 + w])
	
	hits.sort()
	
#	print(hits)
	
	l, r = hits[0]
	for i in range(1, len(hits)):
		nl, nr = hits[i]
		if nl > r + 1:
			for x in range(r + 1, nl):
				if (x, y) not in beacons:
					print(x, y, x * 4000000 + y)
		r = max(r, nr)
	
