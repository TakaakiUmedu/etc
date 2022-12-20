C = {20, 60, 100, 140, 180, 220}

total = 0

v = 1
c = 1
while True:
	l = input().strip()
#	print(c, v, ">", l)
	if c in C:
		total += c * v
		print(c, v)
	if l == "":
		break
	if l == "noop":
		c += 1
	else:
		c += 1
#		print(c, v, ">", l)
		if c in C:
			total += c * v
			print(c, v)
		v += int(l.split()[1])
		c += 1

	

print(total)
