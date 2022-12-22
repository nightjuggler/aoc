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

def get_minmax(tiles):
	min_xs, max_xs, min_ys, max_ys = {}, {}, {}, {}
	for x, y in tiles:
		if y in min_xs:
			if x < min_xs[y]: min_xs[y] = x
			elif x > max_xs[y]: max_xs[y] = x
		else:
			min_xs[y] = max_xs[y] = x
		if x in min_ys:
			if y < min_ys[x]: min_ys[x] = y
			elif y > max_ys[x]: max_ys[x] = y
		else:
			min_ys[x] = max_ys[x] = y
	return min_xs, max_xs, min_ys, max_ys

def move1(tiles, path, x, y, minmax):
	facing = 0
	dxdy = (1, 0), (0, 1), (-1, 0), (0, -1)
	min_xs, max_xs, min_ys, max_ys = minmax
	for move in path:
		if move == 'L': facing = (facing - 1) % 4; continue
		if move == 'R': facing = (facing + 1) % 4; continue
		dx, dy = dxdy[facing]
		if dx:
			min_x, max_x = min_xs[y], max_xs[y]
			for _ in range(int(move)):
				last_x = x
				x += dx
				if x < min_x: x = max_x
				elif x > max_x: x = min_x
				if not tiles[x, y]: x = last_x; break
		else:
			min_y, max_y = min_ys[x], max_ys[x]
			for _ in range(int(move)):
				last_y = y
				y += dy
				if y < min_y: y = max_y
				elif y > max_y: y = min_y
				if not tiles[x, y]: y = last_y; break
	return 1000*(y+1) + 4*(x+1) + facing

def move2(tiles, path, x, y, wrap):
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

def gcd(a, b):
	while b:
		a, b = b, a % b
	return a

def wrap_cube(minmax):
	min_xs, max_xs, min_ys, max_ys = minmax
	assert min(min_xs.values()) == 0
	assert min(min_ys.values()) == 0
	num_cols = max(max_xs.values()) + 1
	num_rows = max(max_ys.values()) + 1
	size = gcd(num_cols, num_rows)
	print('cube size =', size)
	assert (num_cols, num_rows) in ((size*3, size*4), (size*4, size*3))

	wrap = {}
	if size == 4:
		#
		#   A      x
		# BCD    xxx
		#   EF     xx
		#
		for i in range(size):
			# A & C
			wrap[size+i, size-1, 3] = 2*size, i, 0 # top of C -> left of A
			wrap[2*size-1, i, 2] = size+i, size, 1 # left of A -> top of C

			# C & E
			wrap[size+i, 2*size, 1] = 2*size, 3*size-1-i, 0     # bottom of C -> left of E
			wrap[2*size-1, 3*size-1-i, 2] = size+i, 2*size-1, 3 # left of E -> bottom of C

			# A & F
			wrap[3*size, i, 0] = 4*size-1, 3*size-1-i, 2 # right of A -> right of F
			wrap[4*size, 3*size-1-i, 0] = 3*size-1, i, 2 # right of F -> right of A

			# D & F
			wrap[3*size, size+i, 0] = 4*size-1-i, 2*size, 1     # right of D -> top of F
			wrap[4*size-1-i, 2*size-1, 3] = 3*size-1, size+i, 2 # top of F -> right of D

			# A & B
			wrap[i, size-1, 3] = 3*size-1-i, 0, 1 # top of B -> top of A
			wrap[3*size-1-i, -1, 3] = i, size, 1  # top of A -> top of B

			# B & E
			wrap[i, 2*size, 1] = 3*size-1-i, 3*size-1, 3 # bottom of B -> bottom of E
			wrap[3*size-1-i, 3*size, 1] = i, 2*size-1, 3 # bottom of E -> bottom of B

			# B & F
			wrap[-1, size+i, 2] = 4*size-1-i, 3*size-1, 3 # left of B -> bottom of F
			wrap[4*size-1-i, 3*size, 1] = 0, size+i, 0    # bottom of F -> left of B
	elif size == 50:
		#
		#  AB    xx
		#  C     x
		# DE    xx
		# F     x
		#
		for i in range(size):
			# A & F
			wrap[-1, 3*size+i, 2] = size+i, 0, 1 # left of F -> top of A
			wrap[size+i, -1, 3] = 0, 3*size+i, 0 # top of A -> left of F

			# B & F
			wrap[i, 4*size, 1] = 2*size+i, 0, 1    # bottom of F -> top of B
			wrap[2*size+i, -1, 3] = i, 4*size-1, 3 # top of B -> bottom of F

			# E & F
			wrap[size+i, 3*size, 1] = size-1, 3*size+i, 2 # bottom of E -> right of F
			wrap[size, 3*size+i, 0] = size+i, 3*size-1, 3 # right of F -> bottom of E

			# A & D
			wrap[size-1, i, 2] = 0, 3*size-1-i, 0 # left of A -> left of D
			wrap[-1, 3*size-1-i, 2] = size, i, 0  # left of D -> left of A

			# C & D
			wrap[i, 2*size-1, 3] = size, size+i, 0 # top of D -> left of C
			wrap[size-1, size+i, 2] = i, 2*size, 1 # left of C -> top of D

			# B & C
			wrap[2*size+i, size, 1] = 2*size-1, size+i, 2 # bottom of B -> right of C
			wrap[2*size, size+i, 0] = 2*size+i, size-1, 3 # right of C -> bottom of B

			# B & E
			wrap[3*size, size-1-i, 0] = 2*size-1, 2*size+i, 2 # right of B -> right of E
			wrap[2*size, 2*size+i, 0] = 3*size-1, size-1-i, 2 # right of E -> right of B
	return wrap

def main():
	tiles, path = read_input(sys.stdin)
	minmax = get_minmax(tiles)

	# "You begin the path in the leftmost open tile of the top row of tiles."
	y = 0
	x = minmax[0][y]
	while (tile := tiles.get((x, y))) == 0: x += 1
	if tile is None:
		sys.exit('No open tile in the top row!')

	print('Part 1:', move1(tiles, path, x, y, minmax))
	print('Part 2:', move2(tiles, path, x, y, wrap_cube(minmax)))
main()
