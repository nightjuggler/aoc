import re
import sys

def read_input(f):
	node = '([0-9A-Z]{3})'
	pattern = re.compile(f'^{node} = \\({node}, {node}\\)$')

	path = f.readline().strip()
	if not path or path.strip('LR'):
		sys.exit('Line 1 doesn\'t match pattern!')
	if f.readline() != '\n':
		sys.exit('Line 2 doesn\'t match pattern!')

	graph = {}
	for linenum, line in enumerate(f, start=3):
		m = pattern.match(line)
		if not m:
			sys.exit(f'Line {linenum} doesn\'t match pattern!')
		node, left, right = m.groups()
		if node in graph:
			sys.exit(f'Node {node} redefined on line {linenum}!')
		graph[node] = left, right

	return [d == 'R' for d in path], graph

def part1(path, graph):
	pathlen = len(path)
	node = 'AAA'
	steps = 0
	while node != 'ZZZ':
		if node not in graph:
			return f'Node {node} doesn\'t exist!'
		node = graph[node][path[steps % pathlen]]
		steps += 1
	return steps

def gcd(a, b):
	while b:
		a, b = b, a % b
	return a

def part2(path, graph):
	pathlen = len(path)
	total_steps = 1
	for node in graph:
		if node[2] != 'A': continue
		a_node = node
		steps = 0
		seen = {}
		while True:
			i = steps % pathlen
			state = i, node
			if state in seen: break
			seen[state] = steps
			node = graph[node][path[i]]
			steps += 1
		start = seen[state]
		cycle = steps - start
		for (i, z_node), z_steps in seen.items():
			if z_node[2] != 'Z': continue
			if z_steps >= start and z_steps % cycle == 0: break

			a_to_znode = f'{a_node}-{z_node} ({z_steps})'
			a_to_cycle = f'{a_node}-{node}-{node} ({steps})'
			a_to_start = f'{a_node}-{node} ({start})'
			if z_steps < start:
				print(f'{a_to_znode} < {a_to_start}')
			else:
				print(f'{a_to_znode} != {a_to_cycle} - {a_to_start}')
		else:
			return None
		total_steps *= z_steps // gcd(z_steps, total_steps)
	return total_steps

def main():
	path, graph = read_input(sys.stdin)
	print('Part 1:', part1(path, graph))
	print('Part 2:', part2(path, graph))
main()
