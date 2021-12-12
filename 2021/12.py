import re
import sys

def read_input():
	cave_name = '([a-z]{1,2}|[A-Z]{1,2}|start|end)'
	line_pattern = re.compile(f'^{cave_name}-{cave_name}$')
	connections = []
	for line_number, line in enumerate(sys.stdin, start=1):
		m = line_pattern.match(line)
		if not m:
			print(f'Input line {line_number} doesn\'t match pattern!')
			return None
		connections.append(m.groups())
	return connections

def main(verbose=False):
	connections = read_input()
	if not connections: return

	caves = {}
	for a, b in connections:
		conns = caves.get(a)
		if not conns:
			caves[a] = conns = set()
		conns.add(b)
		conns = caves.get(b)
		if not conns:
			caves[b] = conns = set()
		conns.add(a)

	if verbose:
		for cave, conns in caves.items():
			print(cave, '->', ', '.join(sorted(conns)))

	path = []
	num_paths = 0
	visited = {cave: 0 for cave in caves}

	def traverse1(cave):
		if cave != cave.upper():
			if visited[cave]: return
			if cave == 'end':
				nonlocal num_paths
				num_paths += 1
				if verbose:
					path.append('end')
					print(','.join(path))
					path.pop()
				return
		visited[cave] += 1
		path.append(cave)
		for c in sorted(caves[cave]):
			traverse1(c)
		visited[cave] -= 1
		path.pop()

	traverse1('start')
	print('Part 1:', num_paths)

	path = []
	num_paths = 0
	visited = {cave: 0 for cave in caves}

	def traverse2(cave, twice):
		if cave != cave.upper():
			if visited[cave]:
				if twice or cave == 'start': return
				twice = True
			if cave == 'end':
				nonlocal num_paths
				num_paths += 1
				if verbose:
					path.append('end')
					print(','.join(path))
					path.pop()
				return
		visited[cave] += 1
		path.append(cave)
		for c in sorted(caves[cave]):
			traverse2(c, twice)
		visited[cave] -= 1
		path.pop()

	traverse2('start', False)
	print('Part 2:', num_paths)

if __name__ == '__main__':
	main()
