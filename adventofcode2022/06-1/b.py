size = 14

while True:
	l = input().strip()
	
	if l == "":
		break
	
	for i in range(len(l) - size):
		if len(set(l[i: i + size])) == size:
			print(i + size)
			break
	