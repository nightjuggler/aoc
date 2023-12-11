import sys

def read_input():
	lines = [line.rstrip() for line in sys.stdin]
	if any(not line or line.strip('|-LJ7F.S') for line in lines):
		sys.exit('One or more input lines are empty or contain unexpected characters!')

	start = [(x, y) for y, line in enumerate(lines)
			for x, c in enumerate(line) if c == 'S']
	if len(start) != 1:
		sys.exit('The input must contain exactly one starting position!')

	linelen = len(lines[0])
	if any(len(line) != linelen for line in lines):
		sys.exit('The input lines are not all of the same length!')

	return start[0], lines

def part1(start, lines):
	north =  0, -1
	south =  0,  1
	east  =  1,  0
	west  = -1,  0
	pipe_dxdy = {}
	dxdy_pipe = {}
	for pipe, d1, d2 in (
		('|', north, south),
		('-', east, west),
		('L', north, east),
		('J', north, west),
		('7', south, west),
		('F', south, east),
	):
		pipe_dxdy[pipe, -d1[0], -d1[1]] = d2
		pipe_dxdy[pipe, -d2[0], -d2[1]] = d1
		dxdy_pipe[d1, d2] = pipe

	ymax = len(lines)-1
	xmax = len(lines[0])-1
	x, y = start
	start_dxdy = tuple((dx, dy)
		for dx, dy in (north, south, east, west)
		if 0 <= (x2 := x+dx) <= xmax
		if 0 <= (y2 := y+dy) <= ymax
		if (lines[y2][x2], dx, dy) in pipe_dxdy)
	if len(start_dxdy) != 2:
		sys.exit('The starting position must connect to exactly two pipes!')

	pipes = {start: dxdy_pipe[start_dxdy]}
	dx, dy = start_dxdy[0]
	x += dx
	y += dy
	while (x, y) != start:
		try:
			pipes[x, y] = pipe = lines[y][x]
			dx, dy = pipe_dxdy[pipe, dx, dy]
		except (IndexError, KeyError):
			sys.exit(f'Loop broken at x={x}, y={y}!')
		x += dx
		y += dy
	return pipes

def part2(pipes):
	xs = sorted(x for x, y in pipes)
	ys = sorted(y for x, y in pipes)
	xrange = range(xs[0], xs[-1]+1)
	yrange = range(ys[0], ys[-1]+1)
	inside = False
	num_inside = 0
	for x in xrange:
		for y in yrange:
			pipe = pipes.get((x, y))
			if pipe:
				if pipe in '-7J':
					inside = not inside
			elif inside:
				num_inside += 1
	return num_inside

def main():
	pipes = part1(*read_input())
	print('Part 1:', len(pipes)//2)
	print('Part 2:', part2(pipes))
main()
