#C = {20, 60, 100, 140, 180, 220}

def draw():
	l = screen[-1]
	if len(l) >= 40:
		l = []
		screen.append(l)
	if v >= len(l) - 1 and v <= len(l) + 1:
		l.append("#")
	else:
		l.append(".")

screen = [[]]

v = 1
c = 1
while True:
	l = input().strip()
#	print(c, v, ">", l)
	draw()
	if l == "":
		break
	if l == "noop":
		c += 1
	else:
		c += 1
#		print(c, v, ">", l)
		draw()
		v += int(l.split()[1])
		c += 1

	

for l in screen:
	print(*l, sep = "")