N = int(input())

count = 0
for _ in range(N):
	data = input().strip().split(",")
	a, b = map(int, data[0].split("-"))
	c, d = map(int, data[1].split("-"))
	
	if not(b < c or a > d):
		count += 1

print(count)
