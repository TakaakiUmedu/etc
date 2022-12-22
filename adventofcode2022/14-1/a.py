
W = 1000
H = 10

SL = 490
SR = 510

grid = [[False] * W for _ in range(H)]

while (l := input().strip()) != "":
	
	data = []
	for d in l.split(" -> "):
		data.append(tuple(map(int, d.split(","))))
	
#	print(data)
	
	for i in range(len(data) - 1):
		x1, y1 = data[i]
		x2, y2 = data[i + 1]
		while True:
#			print(x1, y1)
			while y1 >= H:
				grid.append([False] * W)
				H += 1
			grid[y1][x1] = True
			SL = min(SL, x1 - 1)
			SR = max(SR, x1 + 1)
			if x1 == x2 and y1 == y2:
				break
			x1 += 0 if x1 == x2 else (1 if x1 < x2 else -1)
			y1 += 0 if y1 == y2 else (1 if y1 < y2 else -1)

for l in grid:
	print(*("#" if l[i] else "." for i in range(SL, SR + 1)), sep = "")

step = 0
while True:
	x = 500
	y = 0
	
	while y < H - 1:
		if not grid[y + 1][x]:
			y += 1
		elif not grid[y + 1][x - 1]:
			y += 1
			x -= 1
		elif not grid[y + 1][x + 1]:
			y += 1
			x += 1
		else:
			grid[y][x] = True
			break
	
	if y == H - 1:
		break
	
	step += 1

print()
for l in grid:
	print(*("#" if l[i] else "." for i in range(SL, SR + 1)), sep = "")

print(step)

