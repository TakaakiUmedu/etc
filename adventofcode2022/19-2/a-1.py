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

def check(states):
	return states
	r = 0
	print("rejecting")
	for s1 in list(states):
		for s2 in states:
			if all(a < c or b < d for a, b, c, d in zip(*s1, *s2)):
				print(s1, "<=", s2)
				states.remove(s1)
				r += 1
				break
	print("rejected", r)
	return states

def search(blueprints):
	robots = (1, 0, 0, 0)
	items = (0, 0, 0, 0)
	
	states = [(robots, items)]
	
	for t in range(24):
		print(f"({t}), {len(states)} ")
		new_states = set()

		
		for robots, items in states:
			new_states.add((robots, tuple(a + b for a, b in zip(robots, items))))
			for needed, robot in blueprints:
				new_items = tuple(a - b for a, b in zip(items, needed))
				if all(v >= 0 for v in new_items):
					t = (tuple(v + (1 if i == robot else 0) for i, v in enumerate(robots)), tuple(a + b for a, b in zip(robots, new_items)))
					new_states.add(t)
		
#		states = check(new_states)
		states = new_states
	
#		for s in states:
#			print(s)
	
#	print(states)
#		break
	return max(items[3] for robots, items in states)


#print(blueprint_table)

total = 0
for i, blueprints in enumerate(blueprint_table):
	print(f"[{i}]")
	s = search(blueprints)
	total += (i + 1) * s
	print(i + 1, s)
	break

print(total)
