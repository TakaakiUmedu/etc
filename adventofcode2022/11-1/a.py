import re

def mul(a, b):
	return a * b

def add(a, b):
	return a + b

monkeys = []
while True:
	if (match := re.match(r"Monkey (\d+):", l := input().strip())) == None:
		break
	
	if match := re.match(r"Starting items: (.*)", l := input().strip()):
		items = list(map(int, match.groups()[0].split(", ")))
		if match := re.match(r"Operation: new = (.*)", l := input().strip()):
			a, op, b = match.groups()[0].split(" ")
			if op == "*":
				op = mul
			elif op == "+":
				op = add
			else:
				raise "hoge"
			if a == "old":
				a = -1
			else:
				a = int(a)
			if b == "old":
				b = -1
			else:
				b = int(b)
			if match := re.match(r"Test: divisible by (\d*)", l := input().strip()):
				d = int(match.groups()[0])
				if match := re.match(r"If true: throw to monkey (\d*)", l := input().strip()):
					t = int(match.groups()[0])
					if match := re.match(r"If false: throw to monkey (\d*)", l := input().strip()):
						f = int(match.groups()[0])
						monkeys.append((items, a, op, b, d, t, f))
					else:
						raise "hoge"
				else:
					raise "hoge"
			else:
				raise "hoge"
		else:
			raise "hoge"
	else:
		print(l)
		raise "hoge"
	input()

counts = [0] * len(monkeys)

for monkey in monkeys:
	print(*monkey[0])

for x in range(20):
	print(f"[{x}]")
	for j, monkey in enumerate(monkeys):
		items, a, op, b, d, t, f = monkey
		i = 0
		while i < len(items):
			counts[j] += 1
			v = items[i]
			va = a if a >= 0 else v
			vb = b if b >= 0 else v
			v = op(va, vb) // 3
			if v % d == 0:
				monkeys[t][0].append(v)
			else:
				monkeys[f][0].append(v)
			i += 1
		monkey[0][:] = []
		
	for monkey in monkeys:
		print(monkey[0])

counts.sort()
print(counts[-1] * counts[-2])
