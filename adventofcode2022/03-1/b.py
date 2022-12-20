N = int(input())

total = 0
for _ in range(N // 3):
	table = {}
	for __ in range(3):
		s = input().strip()
		for c in set(s):
			if c in table:
				table[c] += 1
			else:
				table[c] = 1
	l = [(count, c) for c, count in table.items()]
	l.sort()
	if l[-1][0] != 3 or (len(l) >= 2 and l[-2][0] == 3):
		raise "hoge"
	c = l[-1][1]
	if "A" <= c <= "Z":
		total += ord(c) - ord("A") + 27
	else:
		total += ord(c) - ord("a") + 1	

print(total)