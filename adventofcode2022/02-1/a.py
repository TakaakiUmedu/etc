data = []

import sys
values = sys.stdin.read().replace("\r", "").strip().split("\n")
for l in values:
	a, b = l.split()
	data.append((a, b))

#print(len(data))

hand_table = { "X": "A", "Y": "B", "Z": "C" }
score_table = { "A": 1, "B": 2, "C": 3 }

total = 0
for a, b in data:
	b = hand_table[b]
	total += score_table[b]
	score_table[a]
	if a == b:
		total += 3
	elif (a == "A" and b == "B" or a == "B" and b == "C" or a == "C" and b == "A"):
		total += 6
	else:
		total += 0

#	print(total)

print(total)

