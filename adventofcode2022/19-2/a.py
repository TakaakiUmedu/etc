import re

indexes = {
	"ore": 0,
	"clay": 1,
	"obsidian": 2,
	"geode": 3,
}

blueprint_table = []

while True:
	l = input().strip()
	if l == "":
		break
	
	blueprints = []
	if match := re.match(r"Blueprint (\d+): (.+)", l):
		n, b = match.groups()
		recepies = b.split(". ")
		for m in recepies:
			if match := re.match(r"Each (.+) robot costs ([^.]+)\.?$", m):
				r, c = match.groups()
				d = [0] * len(indexes)
				for i in c.split(" and "):
					n, m = i.split()
					d[indexes[m]] = int(n)
				blueprints.append((d, indexes[r]))
			else:
				raise Exception(m)
	else:
		raise Exception(l)
	
	
	blueprint_table.append(blueprints)

print(len(blueprint_table))

for blueprints in blueprint_table:
	print(len(blueprints))
	for b in blueprints:
		print(*b[0], b[1])

