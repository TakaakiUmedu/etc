
positions = set()

hx = 0
hy = 0
tx = 0
ty = 0
positions.add((tx, ty))
while True:
	l = input().strip()
	if l == "":
		break
	a, b = l.split()
	for i in range(int(b)):
		if a == "R":
			hx += 1
		elif a == "L":
			hx -= 1
		elif a == "D":
			hy += 1
		else:
			hy -= 1
		if max(abs(tx - hx), abs(ty - hy)) > 1:
			if tx == hx:
				ty += 1 if ty < hy else -1
			elif ty == hy:
				tx += 1 if tx < hx else -1
			else:
				tx += 1 if tx < hx else -1
				ty += 1 if ty < hy else -1
		positions.add((tx, ty))
	"""
	for y in range(-5, 6):
		for x in range(-5, 6):
			if x == tx and y == ty:
				print("T", end = "")
			elif x == hx and y == hy:
				print("H", end = "")
			elif x == 0 and y == 0:
				print("s", end = "")
			else:
				print(".", end = "")
		print()
	print()
	"""


for y in range(-5, 6):
	for x in range(-5, 6):
		if (x, y) in positions:
			print("#", end = "")
		else:
			print(".", end = "")
	print()
print(len(positions))
