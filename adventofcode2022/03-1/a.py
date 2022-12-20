N = int(input())

total = 0
for _ in range(N):
	s = input().strip()
	s0 = s[:len(s) // 2]
	s1 = s[len(s) // 2:]
	x0 = set(s0)
	x1 = set(s1)
	for c in x0 & x1:
		if "A" <= c <= "Z":
			total += ord(c) - ord("A") + 27
		else:
			total += ord(c) - ord("a") + 1

print(total)