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

def part1(plan):
	trench = make_trench(plan, 0, 0)
	xs = sorted(x for x, y in trench)
	ys = sorted(y for x, y in trench)
	xrange = range(xs[0], xs[-1]+1)
	yrange = range(ys[0], ys[-1]+1)
	inside = False
	num_inside = 0
	for x in xrange:
		for y in yrange:
			if (pipe := trench.get((x, y))):
				if pipe in '-7J':
					inside = not inside
			elif inside:
				num_inside += 1
	return len(trench) + num_inside

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

def part2(plan):
	trench_len = sum(m for d, m in plan)
	xs, ys, trench = compress_plan(plan)
	xrange = range(len(xs))
	yrange = range(len(ys))
	inside = False
	num_inside = 0
	for x in xrange:
		for y in yrange:
			if (pipe := trench.get((x, y))):
				if pipe in '-7J':
					inside = not inside
			elif inside:
				num_inside += (xs[x] - xs[x-1]) * (ys[y] - ys[y-1])
	return trench_len + num_inside

def main():
	plan1, plan2 = read_input()
	print('Part 1:', part1(plan1))
	print('Part 2:', part2(plan2))
main()
