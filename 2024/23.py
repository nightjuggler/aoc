from collections import defaultdict, deque
import re
import sys

def read_input():
	nodes = defaultdict(set)
	pattern = re.compile('^[a-z]{2}-[a-z]{2}$')
	for line_num, line in enumerate(sys.stdin, start=1):
		if not pattern.match(line):
			sys.exit(f'Line {line_num} doesn\'t match pattern!')
		a = line[0:2]
		b = line[3:5]
		nodes[a].add(b)
		nodes[b].add(a)
	return nodes

def part1(nodes):
	threes = set()
	for node1, conn1 in nodes.items():
		for node2 in conn1:
			for node3 in conn1 & nodes[node2]:
				threes.add(tuple(sorted((node1, node2, node3))))
	return sum(any(node[0] == 't' for node in group) for group in threes)

def part2(nodes):
	q = deque()
	best = 0
	best_groups = []
	seen = set()
	for node, conn in nodes.items():
		q.append((frozenset({node}), conn))
		while q:
			group, conn = q.popleft()
			if group in seen: continue
			seen.add(group)
			size = len(group)
			if size > best:
				best = size
				best_groups = [group]
			elif size == best:
				best_groups.append(group)
			for node in conn:
				q.append((group | {node}, conn & nodes[node]))
	assert len(best_groups) == 1
	return ','.join(sorted(best_groups[0]))

def main():
	nodes = read_input()
	print('Part 1:', part1(nodes))
	print('Part 2:', part2(nodes))

main()
