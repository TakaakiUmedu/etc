grid = []

y = 0
while True:
	l = input().strip()
	if l == "":
		break
	d = []
	x = 0
	for c in l:
		if c == "S":
			d.append(0)
			sx = x
			sy = y
		elif c == "E":
			d.append(25)
			ex = x
			ey = y
		else:
			d.append(ord(c) - ord("a"))
		x += 1
	grid.append(d)
	y += 1

#print(grid, sx, sy, ex, ey)

from queue import deque

H = len(grid)
W = len(grid[0])

queue = deque([(ex, ey)])
dists = [[None] * W for _ in range(H)]
dists[ey][ex] = 0

while queue:
	cx, cy = queue.popleft()
	d = dists[cy][cx] + 1
	h = grid[cy][cx]
	for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
		nx = cx + dx
		ny = cy + dy
		if nx >= 0 and nx < W and ny >= 0 and ny < H:
			g = grid[ny][nx]
			e = dists[ny][nx]
			if (e == None or e > d) and g >= h - 1:
				dists[ny][nx] = d
				queue.append((nx, ny))


for l in grid:
	print(l)

for l in dists:
	print(l)

m = H * W
for l, g in zip(dists, grid):
	for d, h in zip(l, g):
		if d != None and h == 0:
			m = min(m, d)

print(m)
