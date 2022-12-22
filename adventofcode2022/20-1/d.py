
data = []

i = 0
while True:
	l = input().strip()
	if l == "":
		break
	
	data.append([int(l) * 811589153, None, None])
	i += 1

N = len(data)

for i in range(N - 1):
	data[i + 1][1] = data[i]
	data[i][2] = data[i + 1]
data[0][1] = data[-1]
data[-1][2] = data[0]

#print(data)

for _ in range(10):
	for n in range(N):
		cur = data[n]
		v, prv, nxt = cur
		v = v % (N - 1)
		if v == 0:
			continue
		prv[2] = nxt
		nxt[1] = prv
		if v < N // 2:
			for _ in range(v):
				prv = prv[2]
		else:
			for _ in range(N - 1 - v):
				prv = prv[1]
		nxt = prv[2]
		prv[2] = cur
		cur[2] = nxt
		nxt[1] = cur
		cur[1] = prv
		
	#	print(*(v for v, i in data))

cur = data[0]
total = 0
while True:
	if cur[0] == 0:
		for i in range(3):
			for j in range(1000):
				cur = cur[2]
			total += cur[0]
			print(cur[0])
		break
	cur = cur[2]

print(total)
