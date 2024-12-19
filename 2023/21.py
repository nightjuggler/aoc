import argparse
from collections import defaultdict, deque

def read_grid(f):
	grid = [list(map('#.S'.index, row.rstrip())) for row in f]
	size = len(grid)
	assert size and all(len(row) == size for row in grid)
	start = [(x, y) for y, row in enumerate(grid) for x, tile in enumerate(row) if tile == 2]
	assert len(start) == 1
	return grid, start[0]

def part1(steps, grid, start):
	size = len(grid)
	seen = set()
	q = deque()
	q.append((steps, *start))
	num_plots = 0
	while q:
		steps, x, y = q.popleft()
		if (x, y) in seen: continue
		seen.add((x, y))
		if not steps % 2: num_plots += 1
		if not steps: continue
		steps -= 1
		q.extend((steps, x, y) for x, y in ((x+1,y), (x,y+1), (x-1,y), (x,y-1))
			if grid[y % size][x % size])
	return num_plots

def get_seen(grid, start, radius):
	size = len(grid)
	xymin = -radius*size
	xymax = (radius+1)*size-1
	seen = {}
	q = deque()
	q.append((0, *start))
	while q:
		steps, x, y = q.popleft()
		if (x, y) in seen: continue
		if not xymin <= x <= xymax: continue
		if not xymin <= y <= xymax: continue
		seen[x, y] = steps
		steps += 1
		q.extend((steps, x, y) for x, y in ((x+1,y), (x,y+1), (x-1,y), (x,y-1))
			if grid[y % size][x % size])
	return seen

def part2(steps, seen, size):
	core = [(x, y) for y in range(size) for x in range(size) if (x, y) in seen]
	delta = set()
	quads = defaultdict(int)
	dxdy = [(size*dx, size*dy) for dx in (-1,1) for dy in (-1,1)]
	for x, y in core:
		for dx, dy in dxdy:
			qx = x + dx
			qy = y + dy
			q = seen[qx, qy]
			quads[q] += 1
			delta.add(seen[qx+dx, qy] - q)
			delta.add(seen[qx, qy+dy] - q)
	assert len(delta) == 1
	delta = delta.pop()
	assert delta % 2

	num_plots = 0
	# The core and the axes
	dxdy = [(size*dx, size*dy) for dx, dy in ((0,-1), (0,1), (-1,0), (1,0))]
	for x, y in core:
		d = steps - seen[x, y]
		if d >= 0 and not d % 2: num_plots += 1
		for dx, dy in dxdy:
			ax = x
			ay = y
			while True:
				ax += dx
				ay += dy
				a = seen[ax, ay]
				d = steps - a
				if d < 0: break
				if not d % 2: num_plots += 1
				if seen[ax+dx, ay+dy] - a == delta:
					num_plots += (d//delta + d%2)//2
					break
	# The quadrants
	for q, count in quads.items():
		d = steps - q
		if d < 0: continue

		# For the following, delta is expected to be odd.
		# For an example, consider the top-left quadrant:
		#
		# The plots that are reachable are indicated by 1's
		#
		# Case 1: d is odd             Case 2: d is even
		# ----------------             -----------------
		#           0                            1
		#          01                           10
		#         010                          101
		#        0101                         1010
		#       01010                        10101
		#      010101                       101010
		#     0101010                      1010101
		#
		# The width of the bottom row (and the height of the rightmost column)
		# is given by 1 + dd where dd = d//delta. In this example, dd = 6.
		# The number of plots reachable in the bottom row (or rightmost column)
		# is 1 + dd//2 if d is even. The total number of plots reachable in the
		# quadrant is then simply this number squared. If d is odd, this number
		# must then be either added if dd is odd or subtracted if dd is even.

		dd = d//delta
		plots = 1 + dd//2
		plots *= plots + (d%2)*(2*(dd%2)-1)

		# The above expression for plots is simply a more succinct version of the following:
		#	if d % 2:
		#		plots *= plots+1 if dd % 2 else plots-1
		#	else:
		#		plots *= plots

		num_plots += count * plots

	return num_plots

def part2_wrapper(steps2, grid, start, radius):
	size = len(grid)
	seen = get_seen(grid, start, radius)
	if isinstance(steps2, int):
		print('Part 2:', part2(steps2, seen, size))
		return
	for steps in steps2:
		plots = part2(steps, seen, size)
		print(f'In exactly {steps} steps, he can reach {plots} garden plots.')

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('-x', '--example', action='store_true')
	parser.add_argument('--steps1', type=int, default=0)
	parser.add_argument('--steps2', type=int, default=0)
	args = parser.parse_args()
	steps1 = args.steps1
	steps2 = args.steps2

	if args.example:
		suffix = 'example'
		radius = 4
		if not (steps1 or steps2):
			steps2 = 6, 10, 50, 100, 500, 1000, 5000
	else:
		suffix = 'input'
		radius = 2
		if not (steps1 or steps2):
			steps1 = 64
			steps2 = 26501365

	with open(f'data/21.{suffix}') as f:
		grid, start = read_grid(f)
	if steps1:
		print('Part 1:', part1(steps1, grid, start))
	if steps2:
		part2_wrapper(steps2, grid, start, radius)
main()
