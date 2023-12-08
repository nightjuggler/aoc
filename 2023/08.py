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
			print(f'Node {node} doesn\'t exist!')
			return None
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
		steps = 0
		state = {}
		z_steps = None
		z_node = None
		a_node = node
		while True:
			key = steps % pathlen, node
			if key in state: break
			state[key] = steps
			node = graph[node][path[steps % pathlen]]
			steps += 1
			if not z_steps and node[2] == 'Z':
				z_steps = steps
				z_node = node
		if z_steps != steps - state[key]:
			sys.exit(
				f'{a_node}-{z_node} ({z_steps}) != '
				f'{a_node}-{node}-{node} ({steps}) - '
				f'{a_node}-{node} ({state[key]})!'
			)
		total_steps *= z_steps // gcd(z_steps, total_steps)
	return total_steps

def main():
	path, graph = read_input(sys.stdin)
	print('Part 1:', part1(path, graph))
	print('Part 2:', part2(path, graph))
main()
