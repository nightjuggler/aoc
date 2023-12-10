import sys

def read_input():
	lines = []
	start = None
	for y, line in enumerate(sys.stdin):
		line = line.rstrip()
		if not line or line.strip('|-LJ7F.S'):
			sys.exit(f'Input line {y+1} is not valid!')
		x = line.find('S')
		if x >= 0:
			assert not start
			start = x, y
		lines.append(line)
	if not lines:
		sys.exit('No input!')
	linelen = len(lines[0])
	if not all(len(line) == linelen for line in lines):
		sys.exit('Input lines not all of the same length!')
	return start, lines

def part1(start, lines):
	north =  0, -1
	south =  0,  1
	east  =  1,  0
	west  = -1,  0
	pipe_dxdy = {
		'|': (north, south),
		'-': (east, west),
		'L': (north, east),
		'J': (north, west),
		'7': (south, west),
		'F': (south, east),
		'.': ((0,0),),
	}
	opposite = {
		north: south,
		south: north,
		east: west,
		west: east,
	}
	ymax = len(lines)-1
	xmax = len(lines[0])-1
	x, y = start
	start_dxdy = []
	for x2, y2 in ((x+1,y), (x,y+1), (x-1,y), (x,y-1)):
		if x2 < 0 or x2 > xmax: continue
		if y2 < 0 or y2 > ymax: continue
		for dx, dy in pipe_dxdy[lines[y2][x2]]:
			if (x2+dx, y2+dy) == start:
				start_dxdy.append(opposite[dx, dy])
				break
	del pipe_dxdy['.']
	dxdy_pipe = {tuple(sorted(dxdy)): pipe for pipe, dxdy in pipe_dxdy.items()}
	pipes = {start: dxdy_pipe[tuple(sorted(start_dxdy))]}
	dx, dy = start_dxdy[0]
	xy = x+dx, y+dy
	prev_xy = start
	while xy != start:
		x, y = xy
		pipes[xy] = pipe = lines[y][x]
		for dx, dy in pipe_dxdy[pipe]:
			next_xy = x+dx, y+dy
			if next_xy != prev_xy:
				xy, prev_xy = next_xy, xy
				break
	return pipes

def part2(pipes):
	xs = sorted(x for x, y in pipes)
	ys = sorted(y for x, y in pipes)
	xrange = range(xs[0], xs[-1]+1)
	yrange = range(ys[0], ys[-1]+1)
	inout = {
		(None, '-'): (None, True ),
		( '7', '|'): ( '7', False),
		( 'F', '|'): ( 'F', False),
		(None, '7'): ( '7', False),
		(None, 'F'): ( 'F', False),
		( '7', 'L'): (None, True ),
		( 'F', 'L'): (None, False),
		( '7', 'J'): (None, False),
		( 'F', 'J'): (None, True ),
	}
	prev = None
	inside = False
	num_inside = 0
	for x in xrange:
		for y in yrange:
			pipe = pipes.get((x, y))
			if not pipe:
				assert not prev
				if inside:
					num_inside += 1
			else:
				prev, flip = inout[prev, pipe]
				if flip:
					inside = not inside
		assert not prev
		assert not inside
	return num_inside

def main():
	start, lines = read_input()
	pipes = part1(start, lines)
	print('Part 1:', len(pipes)//2)
	print('Part 2:', part2(pipes))
main()
