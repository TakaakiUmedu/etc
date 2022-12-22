from fractions import Fraction

ops = {
	"+": lambda a, b: a + b,
	"-": lambda a, b: a - b,
	"*": lambda a, b: a * b,
	"/": lambda a, b: a / b,
}

# c = a ? b, b = 
ops_rev_l = {
	"+": lambda c, a: c - a,
	"-": lambda c, a: a - c,
	"*": lambda c, a: c / a,
	"/": lambda c, a: a / c,
}

# c = a ? b, a = 
ops_rev_r = {
	"+": lambda c, b: c - b,
	"-": lambda c, b: c + b,
	"*": lambda c, b: c / b,
	"/": lambda c, b: c * b,
}

monkeys = {}

while True:
	l = input().strip()
	if l == "":
		break
	m, d = l.split(": ")
	d = d.split()
	if len(d) == 1:
		monkeys[m] = Fraction(d[0])
	else:
		monkeys[m] = d

cache = {}

def yell(m):
	if m in cache:
		return cache[m]
	d = monkeys[m]
	if type(d) != Fraction and d != None:
		y1 = yell(d[0])
		y2 = yell(d[2])
		if y1 == None or y2 == None:
			d = None
		else:
			d = ops[d[1]](y1, y2)
	cache[m] = d
	return d

def set(m, vc):
	if cache[m] != None:
		raise Exception(m)
	cache[m] = vc
	print(m)
	d = monkeys[m]
	if d == None:
		return
	a, op, b = d
	va = cache[a]
	vb = cache[b]
	if va == None and vb != None:
		set(a, ops_rev_r[op](vc, vb))
	elif va != None and vb == None:
		set(b, ops_rev_l[op](vc, va))
	else:
		raise Exception(m)

monkeys["humn"] = None
for m in monkeys.keys():
	yell(m)

print(cache)

m1 = monkeys["root"][0]
m2 = monkeys["root"][2]
v1 = yell(m1)
v2 = yell(m2)
if v1 == None and v2 != None:
	set(m1, v2)
elif v1 != None and v2 == None:
	set(m2, v1)
else:
	raise Exception("root")

print(cache["humn"])
