import sys

data = sys.stdin.read().replace("\r", "").split("\n\n")

print(data)

data = [sum(int(v) for v in vs.split("\n")) for vs in data]

print(max(data))
