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
	if b == "X":
		if a == "A":
			b = "C"
		elif a == "B":
			b = "A"
		else:
			b = "B"
	elif b == "Y":
		b = a
	else:
		if a == "A":
			b = "B"
		elif a == "B":
			b = "C"
		else:
			b = "A"
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

