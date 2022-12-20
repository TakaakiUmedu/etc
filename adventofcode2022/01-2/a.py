import sys

data = sys.stdin.read().replace("\r", "").split("\n\n")

print(data)

data = [sum(int(v) for v in vs.split("\n")) for vs in data]

data.sort()

print(data[-1] + data[-2] + data[-3])
