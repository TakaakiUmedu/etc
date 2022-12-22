grid = []

while True:
	l = list(input())
	if len(l) > 0 and l[-1] == "\r":
		l.pop()
	l = "".join(l)
	if l == "":
		break
	grid.append(l)

moves = input().strip()

dx = 1
dy = 0

H = len(grid)
W = max(len(l) for l in grid)

y = 0
for i in range(W):
	if grid[0][i] == ".":
		x = i
		break

print(x, y)

def move(x, y, dx, dy):
	if dy == 0:
		x += dx
		while True:
			if x >= len(grid[y]):
				x = 0
			elif x < 0:
				x = len(grid[y]) - 1
			if grid[y][x] == " ":
				x += dx
			else:
				break
		if grid[y][x] == "#":
			return None
		else:
			return (x, y)
	else:
		y += dy
		while True:
			if y >= H:
				y = 0
			elif y < 0:
				y = H - 1
			if x >= len(grid[y]) or grid[y][x] == " ":
				y += dy
			else:
				break
		if grid[y][x] == "#":
			return None
		else:
			return (x, y)

arrows = ">v<^"
dirs = {
	(1, 0): 0,
	(0, 1): 1,
	(-1, 0): 2,
	(0, -1): 3
}

path = {(x, y): arrows[dirs[(dx, dy)]]}

i = 0
while True:
	l = 0
	while i < len(moves) and moves[i] in "0123456789":
		l *= 10
		l += int(moves[i])
		i += 1
	
	for j in range(l):
		n = move(x, y, dx, dy)
		if n == None:
			break
		else:
			x, y = n
		
		path[(x, y)] = arrows[dirs[(dx, dy)]]
#		for p, l in enumerate(grid):
#			print(*(arrows[dirs[(dx, dy)]] if q == x and p == y else c for q, c in enumerate(l)), sep = "")
#		print()
	
	if i < len(moves):
		t = moves[i]
		if t == "L":
			dx, dy = dy, -dx
		else:
			dx, dy = -dy, dx
		if i < len(moves):
			i += 1
		else:
			break
	else:
		break

for p, l in enumerate(grid):
	print(*(path[(q, p)] if (q, p) in path else c for q, c in enumerate(l)), sep = "")
print()


print(y + 1, x + 1, dirs[(dx, dy)])

print(1000 * (y + 1) + 4 * (x + 1) + dirs[(dx, dy)])
