ops = {
	"+": lambda a, b: a + b,
	"-": lambda a, b: a - b,
	"*": lambda a, b: a * b,
	"/": lambda a, b: a / b,
}

monkeys = {}

while True:
	l = input().strip()
	if l == "":
		break
	m, d = l.split(": ")
	d = d.split()
	if len(d) == 1:
		monkeys[m] = int(d[0])
	else:
		monkeys[m] = d

cache = {}

def yell(m):
	if m in cache:
		return cache[m]
	d = monkeys[m]
	if type(d) != int:
		d = ops[d[1]](yell(d[0]), yell(d[2]))
	cache[m] = d
	return d

print(yell("root"))
