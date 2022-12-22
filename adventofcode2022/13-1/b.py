
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

def sort(l):
	for i in range(len(l) - 1):
		for j in range(i, len(l)):
			if check(l[i], l[j]) > 0:
				l[i], l[j] = l[j], l[i]

data = [
	[[2]],
	[[6]],
]
while True:
	l1 = input().strip()
	if l1 == "":
		break
	l2 = input().strip()
	
	data.append(parse(l1))
	data.append(parse(l2))
	
	input()

print(len(data))

sort(data)

for x in data:
	print(x)

print((data.index([[2]]) + 1) * (data.index([[6]]) + 1))
