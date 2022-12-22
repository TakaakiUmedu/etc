
def parse(l):
	i = 0
	cur = ret = []
	stack = []
	
	d = None
	while i < len(l):
#		print(stack, cur)
		c = l[i]
		if c == "[":
			stack.append(cur)
			new_cur = []
			cur.append(new_cur)
			cur = new_cur
		elif c == "," or c == "]":
			if d != None:
				cur.append(d)
				d = None
			if c == "]":
				cur = stack.pop()
		elif "0" <= c <= "9":
			if d != None:
				d *= 10
			else:
				d = 0
			d += ord(c) - ord("0")
		else:
			raise "hoge"
		i += 1
	return cur[0]


def check(x1, x2):
	if type(x1) == int and type(x2) == int:
		return x1 - x2
	elif type(x1) == int and type(x2) == list:
		return check([x1], x2)
	elif type(x1) == list and type(x2) == int:
		return check(x1, [x2])
	else:
		i = 0
		while True:
			if i == len(x1) == len(x2):
				return 0
			elif i == len(x1):
				return -1
			elif i == len(x2):
				return 1
			c = check(x1[i], x2[i])
			if c != 0:
				return c
			else:
				i += 1


total = 0
t = 1
while True:
	l1 = input().strip()
	if l1 == "":
		break
	l2 = input().strip()
	
	x1 = parse(l1)
	x2 = parse(l2)
	
#	print(x1)
#	print(x2)
	if check(x1, x2) <= 0:
		print(t)
		total += t
	t += 1
	
	input()

print(total)
