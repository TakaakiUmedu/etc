
positions = set()
L = 10

xs = [0] * L
ys = [0] * L
positions.add((xs[-1], ys[-1]))
while True:
	l = input().strip()
	if l == "":
		break
	a, b = l.split()
	for i in range(int(b)):
		if a == "R":
			xs[0] += 1
		elif a == "L":
			xs[0] -= 1
		elif a == "D":
			ys[0] += 1
		else:
			ys[0] -= 1
		for t in range(1, L):
			h = t - 1
			if max(abs(xs[t] - xs[h]), abs(ys[t] - ys[h])) > 1:
				if xs[t] == xs[h]:
					ys[t] += 1 if ys[t] < ys[h] else -1
				elif ys[t] == ys[h]:
					xs[t] += 1 if xs[t] < xs[h] else -1
				else:
					xs[t] += 1 if xs[t] < xs[h] else -1
					ys[t] += 1 if ys[t] < ys[h] else -1
		positions.add((xs[-1], ys[-1]))
	"""
	for y in range(-5, 6):
		for x in range(-5, 6):
			if x == xs[t] and y == ys[t]:
				print("T", end = "")
			elif x == xs[h] and y == ys[h]:
				print("H", end = "")
			elif x == 0 and y == 0:
				print("s", end = "")
			else:
				print(".", end = "")
		print()
	print()
	"""

for y in range(-10, 10):
	for x in range(-10, 10):
		if (x, y) in positions:
			print("#", end = "")
		else:
			print(".", end = "")
	print()
print(len(positions))
