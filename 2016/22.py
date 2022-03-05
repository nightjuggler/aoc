from collections import deque
from operator import itemgetter
import re
import sys

def sanity_check(nodes):
	if not nodes: return

	prev_x, max_y = nodes[-1][:2]
	prev_y = max_y + 1

	for x, y, size, used, avail, percent_used in nodes[::-1]:
		assert size == used + avail
		assert int(100 * used / size) == percent_used

		if x == prev_x:
			assert y == prev_y - 1
		else:
			assert x == prev_x - 1 and prev_y == 0 and y == max_y
		prev_x = x
		prev_y = y

	assert prev_x == 0 == prev_y

def read_input(f):
	n = '([1-9][0-9]*|0)'
	pattern = re.compile(f'^/dev/grid/node-x{n}-y{n} +{n}T +{n}T +{n}T +{n}%$')

	nodes = []
	for line_num, line in enumerate(f, start=1):
		if m := pattern.match(line):
			nodes.append(tuple(map(int, m.groups())))
		elif nodes or line_num > 2:
			sys.exit(f"Input line {line_num} doesn't match pattern!")
	return nodes

# Simple, but slower
def part1(nodes):
	get_used = itemgetter(3)
	get_avail = itemgetter(4)

	return sum(sum(used <= get_avail(n2) and n1 is not n2 for n2 in nodes)
		for n1 in nodes if (used := get_used(n1)))

# More complicated, but faster
def part1(nodes):
	get_used = itemgetter(3)
	get_avail_used = itemgetter(4, 3)

	used_sorted = sorted(filter(None, map(get_used, nodes)), reverse=True)
	avail_sorted = sorted(map(get_avail_used, nodes), reverse=True)

	if not used_sorted: return 0

	num_viable = 0
	len_used = len(used_sorted)
	used_sorted = enumerate(used_sorted)
	i, used = next(used_sorted)

	for avail, avail_used in avail_sorted:
		if used > avail:
			for i, used in used_sorted:
				if used <= avail: break
			else:
				break
		num_viable += len_used - i - int(0 < avail_used <= used)

	return num_viable

def part2(nodes):
	if not nodes:
		return None

	get_used = itemgetter(3)
	get_avail = itemgetter(4)

	x, y = nodes[-1][:2]
	size_x = x + 1
	size_y = y + 1

	data_xy = (x, 0)
	from_xy = []
	to_xy = set()

	for i, used in enumerate(map(get_used, nodes)):
		if not used: continue
		px, py = divmod(i, size_y)
		for x, y in ((px+1, py), (px, py+1), (px-1, py), (px, py-1)):
			if not (0 <= x < size_x): continue
			if not (0 <= y < size_y): continue
			if used <= get_avail(nodes[x*size_y+y]):
				from_xy.append((px, py))
				to_xy.add((x, y))

	assert len(to_xy) == 1
	x, y = to_xy = to_xy.pop()
	size, used = nodes[x*size_y+y][2:4]
	assert used == 0

	fits = {to_xy}
	sizes = [size]
	useds = []
	q = deque()
	q.append((x, y, size))

	while q:
		px, py, psize = q.popleft()
		for xy in ((px+1, py), (px, py+1), (px-1, py), (px, py-1)):
			x, y = xy
			if not (0 <= x < size_x): continue
			if not (0 <= y < size_y): continue
			if xy in fits: continue
			size, used = nodes[x*size_y+y][2:4]
			if used <= psize:
				fits.add(xy)
				sizes.append(size)
				useds.append(used)
				q.append((x, y, size))

	sizes.sort()
	min_size = sizes[0]
	max_size = sizes[-1]
	useds.sort()
	min_used = useds[0]
	max_used = useds[-1]

	assert min_size > max_used
	assert max_size < min_used*2

	seen = {(to_xy, data_xy)}
	for xy in from_xy:
		q.append((1, xy, to_xy, data_xy))
	while q:
		steps, from_xy, to_xy, data_xy = q.popleft()
		if from_xy == data_xy:
			if to_xy == (0, 0): return steps
			data_xy = to_xy
		state = (from_xy, data_xy)
		if state in seen: continue
		seen.add(state)

		x, y = from_xy
		steps += 1
		for xy in ((x+1, y), (x, y+1), (x-1, y), (x, y-1)):
			if xy != to_xy and xy in fits:
				q.append((steps, xy, from_xy, data_xy))
	return None

def main():
	nodes = read_input(sys.stdin)
	sanity_check(nodes)

	print('Part 1:', part1(nodes))
	print('Part 2:', part2(nodes))

if __name__ == '__main__':
	main()
