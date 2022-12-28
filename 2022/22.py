import re
import sys

def err(line_num): sys.exit(f'Line {line_num} doesn\'t match expected pattern!')

def read_input(f):
	tiles, path = {}, []
	pattern = re.compile('^( *)([#.]+)$')
	for y, line in enumerate(f):
		if not (m := pattern.match(line)):
			if line.strip(): err(y + 1)
			line = f.readline().strip()
			path = re.findall('L|R|[1-9][0-9]*', line)
			if line != ''.join(path): err(y + 2)
			break
		tiles.update(((x, y), '#.'.index(c))
			for x, c in enumerate(m.group(2), start=len(m.group(1))))
	return tiles, path

def wrap_plane(tiles):
	minmax_x, minmax_y = {}, {}
	for x, y in tiles:
		if m := minmax_x.get(y):
			if   x < m[0]: m[0] = x
			elif x > m[1]: m[1] = x
		else:
			minmax_x[y] = [x, x]
		if m := minmax_y.get(x):
			if   y < m[0]: m[0] = y
			elif y > m[1]: m[1] = y
		else:
			minmax_y[x] = [y, y]
	wrap = {}
	wrap.update(((max_x+1, y, 0), (min_x, y, 0)) for y, (min_x, max_x) in minmax_x.items())
	wrap.update(((min_x-1, y, 2), (max_x, y, 2)) for y, (min_x, max_x) in minmax_x.items())
	wrap.update(((x, max_y+1, 1), (x, min_y, 1)) for x, (min_y, max_y) in minmax_y.items())
	wrap.update(((x, min_y-1, 3), (x, max_y, 3)) for x, (min_y, max_y) in minmax_y.items())
	return wrap

def coords(size, x, y, facing, offmap):
	d1 = 1 - facing//2
	if not offmap: facing = (facing + 2) % 4
	d2 = facing//2

	if facing % 2:
		cx = x*size
		cy = (y + d1)*size - d2
		return [(x, cy, facing) for x in range(cx, cx+size)]

	cx = (x + d1)*size - d2
	cy = y*size
	return [(cx, y, facing) for y in range(cy, cy+size)]

def gcd(a, b):
	while b:
		a, b = b, a % b
	return a

def wrap_cube(tiles):
	num_cols = max(x for x, y in tiles) + 1
	num_rows = max(y for x, y in tiles) + 1
	size = gcd(num_cols, num_rows)
	assert sorted((num_cols // size, num_rows // size)) == [3, 4]

	for ty in range(0, num_rows, size):
		for tx in range(0, num_cols, size):
			on = (tx, ty) in tiles
			assert all(((x, y) in tiles) is on
				for y in range(ty, ty + size)
					for x in range(tx, tx + size))
	i = iter('123456')
	shape = '|'.join([''.join([next(i) if (x, y) in tiles else '.'
		for x in range(0, num_cols, size)])
			for y in range(0, num_rows, size)])
	shapes = {
		'..1.|234.|..56': (
		#   A      1
		# BCD    234
		#   EF     56
		'1<3^',  #   left of A ->    top of C
		'3v5<-', # bottom of C ->   left of E reversed
		'1>6>-', #  right of A ->  right of F reversed
		'4>6^-', #  right of D ->    top of F reversed
		'1^2^-', #    top of A ->    top of B reversed
		'2v5v-', # bottom of B -> bottom of E reversed
		'2<6v-', #   left of B -> bottom of F reversed
		),
		'.12|.3.|45.|6..': (
		#  AB    12
		#  C     3
		# DE    45
		# F     6
		'1^6<',  #    top of A ->   left of F
		'2^6v',  #    top of B -> bottom of F
		'5v6>',  # bottom of E ->  right of F
		'1<4<-', #   left of A ->   left of D reversed
		'3<4^',  #   left of C ->    top of D
		'2v3>',  # bottom of B ->  right of C
		'2>5>-', #  right of B ->  right of E reversed
		),
	}
	wrap = {}
	sides = [(x, y) for y, row in enumerate(shape.split('|')) for x, side in enumerate(row) if side != '.']
	for s1,d1,s2,d2,*rev in shapes[shape]:
		side1 = *sides['123456'.index(s1)], '>v<^'.index(d1)
		side2 = *sides['123456'.index(s2)], '>v<^'.index(d2)
		pos1 = coords(size, *side1, True)
		pos2 = coords(size, *side2, False)
		if rev: pos2 = pos2[::-1]
		wrap.update(zip(pos1, pos2))
		pos1 = coords(size, *side2, True)
		pos2 = coords(size, *side1, False)
		if rev: pos2 = pos2[::-1]
		wrap.update(zip(pos1, pos2))
	return wrap

def follow(tiles, path, x, y, wrap):
	facing = 0
	dxdy = (1, 0), (0, 1), (-1, 0), (0, -1)
	for move in path:
		if move == 'L': facing = (facing - 1) % 4; continue
		if move == 'R': facing = (facing + 1) % 4; continue
		for _ in range(int(move)):
			dx, dy = dxdy[facing]
			pos = x + dx, y + dy, facing
			pos = wrap.get(pos, pos)
			if not tiles[pos[:2]]: break
			x, y, facing = pos
	return 1000*(y+1) + 4*(x+1) + facing

def main():
	tiles, path = read_input(sys.stdin)

	# "You begin the path in the leftmost open tile of the top row of tiles."
	x = min((x for (x, y), tile in tiles.items() if not y and tile), default=None)
	if x is None:
		sys.exit('No open tile in the top row!')

	print('Part 1:', follow(tiles, path, x, 0, wrap_plane(tiles)))
	print('Part 2:', follow(tiles, path, x, 0, wrap_cube(tiles)))
main()
