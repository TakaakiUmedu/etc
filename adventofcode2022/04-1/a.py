N = int(input())

count = 0
for _ in range(N):
	data = input().strip().split(",")
	a, b = map(int, data[0].split("-"))
	c, d = map(int, data[1].split("-"))
	
	if (a <= c and b >= d) or (c <= a and d >= b):
		count += 1

print(count)
