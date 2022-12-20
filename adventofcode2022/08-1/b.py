
data = []

while True:
	l = input().strip()
	if l == "":
		break
	data.append(list(map(int, l)))

W = len(data[0])
H = len(data)

best_score = 1
for y in range(H):
	for x in range(W):
		score = 1
		h = data[y][x]
		for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
			l = 0
			cx = x + dx
			cy = y + dy
			while True:
				if cx >= 0 and cx < W and cy >= 0 and cy < H:
					l += 1
					if data[cy][cx] > h:
						break
					if data[cy][cx] == h:
						break
				else:
					break
				cx += dx
				cy += dy
#			print(x, y, l)
			score *= l
		best_score = max(best_score, score)
		print(">", x, y, score)

print(best_score)


