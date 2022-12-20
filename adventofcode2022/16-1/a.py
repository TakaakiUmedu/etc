import re

def read():
	flows = {}
	graph = {}
	while True:
		line = input()
		match = re.match(r"^Valve (..) has flow rate=(\d+); tunnels? leads? to valves? (.+)$", line)
		if match:
			a, b, c = match.groups()
			if a in flows:
				raise Error()
			if int(b) > 0:
				flows[a] = int(b)
			graph[a] = [v.strip() for v in c.split(", ")]
		else:
			break
	
	indexes = {}
	flows_list = []
	for v, f in flows.items():
		indexes[v] = len(indexes)
		flows_list.append(f)
	
	print(indexes)

	for v in graph.keys():
		if v not in indexes:
			indexes[v] = len(indexes)
	
	print(indexes)
	
	graph_list = [None] * len(indexes)
	for v, l in graph.items():
		i = indexes[v]
		graph_list[i] = [indexes[n] for n in l]
	
	return flows_list, graph_list, indexes['AA']

from heapq import heappush, heappop

flows, graph, start = read()

T = 30
N = len(flows)
M = len(graph)

amounts = [None] * (((M << N) + (1 << N)) * T)
amounts[((start << N) + 0) * T] = 0
queue = [(0, 0, start, 0)]

while queue:
#	print(queue)
	a, t, cur, valves = heappop(queue)
	if a != amounts[((cur << N) + valves) * T + t]:
		continue
	t += 1
	if t >= T:
		continue
	if cur < N and (valves & (1 << cur))== 0:
		v = (valves | (1 << cur))
		s = ((cur << N) + v) * T + t
		new_a = a + flows[cur] * (T - t)
		if amounts[s] == None or amounts[s] < new_a:
			amounts[s] = new_a
			heappush(queue, (new_a, t, cur, v))
	for n in graph[cur]:
		s = ((n << N) + valves) * T + t
		if amounts[s] == None or amounts[s] < a:
			amounts[s] = a
			heappush(queue, (a, t, n, valves))

top_value = 0

for s, a in enumerate(amounts):
#	f = 0
#	for i in range(N):
#		if (s & (1 << i)) != 0:
#			f += flows[i]
	if a != None:
		top_value = max(top_value, a)

print(top_value)
