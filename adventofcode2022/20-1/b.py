
data = []

i = 0
while True:
	l = input().strip()
	if l == "":
		break
	
	data.append((int(l) * 811589153, i))
	i += 1

N = len(data)

positions = list(range(N))

print(data)

for _ in range(10):
	for n in range(N):
		i = positions[n]
		v1, j1 = data[i]
		if v1 == 0:
			continue
		
		x = i + v1 % (N - 1)
		m = x - i
		if m < 0:
			d = -1
		else:
			d = 1
		
	#	print(v1, m)
		
		for _ in range(abs(m)):
			k = (i + d) % N
			v2, j2 = data[k]
			
			data[i], data[k] = data[k], data[i]
			positions[n], positions[j2] = positions[j2], positions[n]
			i = k
		
	#	print(*(v for v, i in data))

i0 = None
for i in range(N):
	if data[i][0] == 0:
		i0 = i
		break
print(*(data[(i + i0) % N][0] for i in (1000, 2000, 3000)))
print(sum(data[(i + i0) % N][0] for i in (1000, 2000, 3000)))

