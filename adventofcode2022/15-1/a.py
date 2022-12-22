import re
data = []

y = int(input())

def dist(x1, y1, x2, y2):
	return abs(x2 - x1) + abs(y2 - y1)

while (l := input().strip()) != "":
	if match := re.match(r"Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)", l):
		x1, y1, x2, y2 = tuple(map(int, match.groups()))
		data.append((x1, y1, x2, y2, dist(x1, y1, x2, y2)))
	else:
		raise Exception(l)

#print(data)

hits = []
for x1, y1, x2, y2, d in data:
	w = d - abs(y1 - y)
	if w > 0:
		hits.append([x1 - w, x1 + w])

L = min(l for l, r in hits)

for i in range(len(hits)):
	hits[i][0] -= L
	hits[i][1] -= L

R = max(r for l, r in hits)
row = [False] * (R + 1)
for l, r in hits:
	for i in range(l, r + 1):
		row[i] = True

#print(*("#" if c else "." for c in row), sep = "")

for x1, y1, x2, y2, d in data:
	if y2 == y:
		x2 -= L
		if x2 >= 0 and x2 <= R:
			row[x2] = False
#print(*("#" if c else "." for c in row), sep = "")

count = sum(1 if c else 0 for c in row)

print(count)
