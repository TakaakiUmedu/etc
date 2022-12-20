import re

data = []
while True:
	l = input()
	
	if re.match(r"\s+(\d+\s+)+", l):
		break
	
	values = []
	for i in range(1, len(l), 4):
		values.append(l[i])
	
	data.append(values)

data.reverse()
data = list(map(list, zip(*data)))
for l in data:
	while len(l) > 0 and l[-1] == " ":
		l.pop()
#print(data)

input()
while True:
	l = input().strip()
	
	if l == "":
		break
	if (match := re.match(r"move (\d+) from (\d+) to (\d+)", l)) == None:
		break
	c, f, t = map(int, match.groups())
	
	f -= 1
	t -= 1
#	for _ in range(c):
#		data[t].append(data[f].pop())
	data[t].extend(data[f][-c:])
	data[f][-c:] = []

	print(data)

print(*(l[-1] for l in data), sep = "")
