import sys

def print_paths(node, depth=0):
	directions, branches, node = node
	for d in directions:
		print('\t'*depth, d)
	if branches:
		for node in branches:
			print_paths(node, depth+1)
	elif node:
		print_paths(node, depth+1)
	else:
		print('end')

def parse_regex(regex, i, n, parent):
	node = ['', [], parent[2]]
	parent[1].append(node)
	j = i + 1
	while i < n:
		i += 1
		c = regex[i]
		if c in 'NSEW': continue
		if c == '(':
			node[0] = regex[j:i]
			node[2] = ['', [], parent[2]]
			i = parse_regex(regex, i, n, node)
			node = node[2]
			j = i + 1
			continue
		if c == '|':
			node[0] = regex[j:i]
			node = ['', [], parent[2]]
			parent[1].append(node)
			j = i + 1
			continue
		if c == ')' or c == '$':
			node[0] = regex[j:i]
			return i
		print(f'Unexpected character \'{c}\' at position {i}!')
	return i

def main():
	regex = sys.stdin.readline().rstrip()
	n = len(regex) - 1
	assert n > 0
	assert regex[0] == '^'
	assert regex[n] == '$'
	parent = ['', [], None]
	i = parse_regex(regex, 0, n, parent)
	assert i == n

	rooms = {}

	def traverse(node, y, x, doors):
		if len(node) == 3:
			node.append({})
		directions, branches, node, seen = node
		yx = (y, x)
		prev = seen.get(yx)
		if prev and doors >= prev:
			return
		seen[yx] = doors
		for d in directions:
			if   d == 'N': y -= 1
			elif d == 'S': y += 1
			elif d == 'E': x += 1
			elif d == 'W': x -= 1
			doors += 1
			yx = (y, x)
			min_doors = rooms.get(yx)
			if not min_doors or doors < min_doors:
				rooms[yx] = doors
		if branches:
			for node in branches:
				traverse(node, y, x, doors)
		elif node:
			traverse(node, y, x, doors)

	traverse(parent, 0, 0, 0)

	print('Part 1:', max(rooms.values()))
	n = 0
	for sp in rooms.values():
		if sp >= 1000: n += 1
	print('Part 2:', n)

if __name__ == '__main__':
	main()
