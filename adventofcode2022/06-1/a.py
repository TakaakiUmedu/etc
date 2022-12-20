while True:
	l = input().strip()
	
	if l == "":
		break
	
	for i in range(len(l) - 4):
		if len(set(l[i: i + 4])) == 4:
			print(i + 4)
			break
	