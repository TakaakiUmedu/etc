
data = []

while True:
	l = input().strip()
	if l == "":
		break
	data.append(list(map(int, l)))

W = len(data[0])
H = len(data)

visible = [[0] * W for _ in range(H)]

def update(x, y):
	global h
	if h < data[y][x]:
		visible[y][x] = 1
		h = data[y][x]

for x in range(W):
	h = -1
	for y in range(H):
		update(x, y)

	h = -1
	for y in range(H - 1, -1, -1):
		update(x, y)

for y in range(H):
	h = -1
	for x in range(W):
		update(x, y)

	h = -1
	for x in range(W - 1, -1, -1):
		update(x, y)

for l in visible:
	print(l)

print(sum(sum(l) for l in visible))

