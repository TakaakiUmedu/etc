
total = 70000000
needed = 30000000

root = {}
stack = [root]

used = 0
while True:
	l = input().strip()
	if l == "":
		break
	if l[0] == "$":
		cs = l.split(" ")
		if len(cs) == 3:
			if cs[2] == "..":
				stack.pop()
			elif cs[2] == "/":
				while len(stack) > 1:
					stack.pop()
			else:
				stack.append(stack[-1][cs[2]])
		else:
			pass
	else:
		s, f = l.split(" ")
		if s == "dir":
			stack[-1][f] = {}
		else:
			stack[-1][f] = int(s)
			used += int(s)

targets = []

def calc(dir):
	size = 0
	for f, s in dir.items():
		if type(s) == dict:
			size += calc(s)
		else:
			size += s
	if total - (used - size) >= needed:
		targets.append(size)
	return size

calc(root)

print(used, needed)
print(min(targets))
