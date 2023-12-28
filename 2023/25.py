from collections import defaultdict, deque
import sys

def read_input():
	graph = defaultdict(set)
	for line in sys.stdin:
		lhs, rhs = line.split(':')
		for name in rhs.split():
			graph[lhs].add(name)
			graph[name].add(lhs)
	return graph

def get_size(graph, node):
	seen = set()
	q = deque()
	q.append(node)
	while q:
		node = q.popleft()
		if node in seen: continue
		seen.add(node)
		q.extend(graph[node])
	return len(seen)

def solve(graph):
	q = deque()
	wires = defaultdict(int)
	for node in graph:
		seen = {}
		q.append((0, node, None))
		while q:
			step, node, conn = q.popleft()
			if info := seen.get(node):
				if step == info[0]:
					info.append(conn)
			else:
				seen[node] = [step, conn]
				q.extend((step+1, conn, node) for conn in graph[node])
		for node, info in seen.items():
			if not info.pop(0): continue
			n = 1 / len(info)
			for conn in info:
				wire = (conn, node) if conn < node else (node, conn)
				wires[wire] += n

	wires = [(count, wire) for wire, count in wires.items()]
	wires.sort(reverse=True)
	for count, (node1, node2) in wires[:3]:
		print(f'Removing {node1}-{node2} ({count})')
		graph[node1].remove(node2)
		graph[node2].remove(node1)

	size1 = get_size(graph, wires[0][1][0])
	size2 = get_size(graph, wires[0][1][1])
	return size1, size2, size1 * size2

print(solve(read_input()))
