import sys

def part1(bugs):
	def is_bug(x, y):
		n = sum(xy in bugs for xy in ((x+1,y), (x,y+1), (x-1,y), (x,y-1)))
		return n == 1 or n == 2 and (x, y) not in bugs

	ratings = set()
	while not (rating := sum(2**(y*5+x) for x, y in bugs)) in ratings:
		ratings.add(rating)
		bugs = {(x, y)
			for y in range(5)
			for x in range(5)
			if is_bug(x, y)}
	return rating

def get_neighbors(x, y):
	n = []
	# left
	if   x == 0:            n.append((-1, 1, 2))
	elif x == 3 and y == 2: n.extend((1, 4, i) for i in range(5))
	else:                   n.append((0, x-1, y))
	# right
	if   x == 4:            n.append((-1, 3, 2))
	elif x == 1 and y == 2: n.extend((1, 0, i) for i in range(5))
	else:                   n.append((0, x+1, y))
	# up
	if   y == 0:            n.append((-1, 2, 1))
	elif y == 3 and x == 2: n.extend((1, i, 4) for i in range(5))
	else:                   n.append((0, x, y-1))
	# down
	if   y == 4:            n.append((-1, 2, 3))
	elif y == 1 and x == 2: n.extend((1, i, 0) for i in range(5))
	else:                   n.append((0, x, y+1))
	return n

def part2(bugs, steps):
	bugs = {(0, x, y) for x, y in bugs}
	neighbors = [[get_neighbors(x, y) for x in range(5)] for y in range(5)]
	neighbors[2][2] = None # should never be accessed

	for _ in range(steps):
		done = set()
		new_bugs = set()
		for d1, x1, y1 in bugs:
			for d2, x2, y2 in neighbors[y1][x1]:
				d2 += d1
				pos = d2, x2, y2
				if pos in done: continue
				done.add(pos)
				n = sum((d3+d2, x3, y3) in bugs for d3, x3, y3 in neighbors[y2][x2])
				if n == 1 or n == 2 and pos not in bugs:
					new_bugs.add(pos)
		bugs = new_bugs

	return len(bugs)

def main():
	steps = int(sys.argv[1]) if len(sys.argv) > 1 else 200

	lines = [line.rstrip() for line in sys.stdin]
	assert len(lines) == 5
	assert all(len(line) == 5 and not line.strip('#.') for line in lines)
	assert lines[2][2] == '.'
	bugs = {(x, y)
		for y, line in enumerate(lines)
		for x, c in enumerate(line)
		if c == '#'}

	print('Part 1:', part1(bugs))
	print('Part 2:', part2(bugs, steps))
main()
