import re
import sys

dxdy = (
	( 1,  0), # 0 => east
	( 0,  1), # 1 => south
	(-1,  0), # 2 => west
	( 0, -1), # 3 => north
)
pipes = {
	(0, 0): '-', (1, 0): 'L', (2, 0): '-', (3, 0): 'F',
	(0, 1): '7', (1, 1): '|', (2, 1): 'F', (3, 1): '|',
	(0, 2): '-', (1, 2): 'J', (2, 2): '-', (3, 2): '7',
	(0, 3): 'J', (1, 3): '|', (2, 3): 'L', (3, 3): '|',
}

def read_input():
	pattern = re.compile('^([RDLU]) ([1-9][0-9]*) \\(#([0-9a-f]{6})\\)$')
	plan1 = []
	plan2 = []
	for linenum, line in enumerate(sys.stdin, start=1):
		m = pattern.match(line)
		if not m:
			sys.exit(f'Input line {linenum} doesn\'t match pattern!')
		direction, meters, color = m.groups()
		plan1.append(('RDLU'.index(direction), int(meters)))
		plan2.append((int(color[5], base=16), int(color[:5], base=16)))
	return plan1, plan2

def make_trench(plan, start_x, start_y):
	x = start_x
	y = start_y
	trench = {}
	last_d = plan[-1][0]
	for d, m in plan:
		trench[x, y] = pipes[last_d, d]
		dx, dy = dxdy[d]
		pipe = '-' if dx else '|'
		for i in range(m-1):
			x += dx
			y += dy
			trench[x, y] = pipe
		x += dx
		y += dy
		last_d = d
	assert x == start_x and y == start_y
	return trench

def solve_uncompressed(plan):
	trench = make_trench(plan, 0, 0)
	xs = sorted(x for x, y in trench)
	ys = sorted(y for x, y in trench)
	xrange = range(xs[0], xs[-1]+1)
	yrange = range(ys[0], ys[-1]+1)
	num_points = len(trench)
	inside = False
	for x in xrange:
		for y in yrange:
			if (pipe := trench.get((x, y))):
				if pipe in '-7J':
					inside = not inside
			elif inside:
				num_points += 1
	return num_points

def coord_map(xs):
	xs = sorted(set(xs))
	xlist = [xs[0]]
	for i in range(1, len(xs)):
		if xs[i]-1 > xs[i-1]:
			xlist.append(xs[i]-1)
		xlist.append(xs[i])
	return xlist, {x: i for i, x in enumerate(xlist)}

def compress_plan(plan):
	xs = []
	ys = []
	x = y = 0
	for d, m in plan:
		dx, dy = dxdy[d]
		x += dx * m
		y += dy * m
		xs.append(x)
		ys.append(y)
	assert x == y == 0

	xs, xmap = coord_map(xs)
	ys, ymap = coord_map(ys)

	new_plan = []
	for d, m in plan:
		dx, dy = dxdy[d]
		if dx:
			x2 = x + dx * m
			new_plan.append((d, abs(xmap[x2]-xmap[x])))
			x = x2
		else:
			y2 = y + dy * m
			new_plan.append((d, abs(ymap[y2]-ymap[y])))
			y = y2

	return xs, ys, make_trench(new_plan, xmap[0], ymap[0])

def solve_compressed(plan):
	xs, ys, trench = compress_plan(plan)
	xrange = range(len(xs))
	yrange = range(len(ys))
	num_points = sum(m for d, m in plan)
	inside = False
	for x in xrange:
		for y in yrange:
			if (pipe := trench.get((x, y))):
				if pipe in '-7J':
					inside = not inside
			elif inside:
				num_points += (xs[x] - xs[x-1]) * (ys[y] - ys[y-1])
	return num_points

def solve_shoelace(plan):
	#
	# (1) Get the number of boundary points by adding up the distances
	#     specified in the plan.
	# (2) Use the shoelace formula to calculate the area of the polygon:
	#     https://en.wikipedia.org/wiki/Shoelace_formula
	# (3) Use Pick's theorem to get the number of interior points based
	#     on (1) and (2): https://en.wikipedia.org/wiki/Pick's_theorem
	# (4) Return the sum of (3) (the number of interior points) and (1)
	#     (the number of boundary points).
	#
	area = 0
	b = sum(m for d, m in plan)
	x1 = y1 = 0
	for d, m in plan:
		dx, dy = dxdy[d]
		x2 = x1 + dx * m
		y2 = y1 + dy * m
		area += x1*y2 - x2*y1
		x1 = x2
		y1 = y2
	area = abs(area)//2
	return area - b//2 + 1 + b

def main():
	plan1, plan2 = read_input()
	print('Part 1:', solve_uncompressed(plan1), '(uncompressed)')
	print('Part 1:', solve_compressed(plan1), '(compressed)')
	print('Part 1:', solve_shoelace(plan1), '(shoelace)')
	print('Part 2:', solve_compressed(plan2), '(compressed)')
	print('Part 2:', solve_shoelace(plan2), '(shoelace)')
main()
