import sys

def read_map():
	lines = [line.strip() for line in sys.stdin]
	size = len(lines)
	if not (size and all(len(line) == size and not line.strip('#.^') for line in lines)):
		sys.exit('The input is not valid!')
	start = None
	obstacles = [False]*(size*size)
	for y, line in enumerate(lines):
		for x, c in enumerate(line):
			if c == '#':
				obstacles[y*size + x] = True
			elif c == '^':
				if start:
					sys.exit('More than one start position!')
				start = x, y
	if not start:
		sys.exit('Missing start position!')
	return start, size, obstacles

def main():
	start, size, obstacles = read_map()

	def move(x, y, dx, dy, seen):
		xy = y*size + x
		dxdy = 1<<(3*(dx+1)+dy)
		while not (seen[xy] & dxdy):
			seen[xy] |= dxdy
			nx = x + dx
			ny = y + dy
			if not (0 <= nx < size and 0 <= ny < size):
				return False
			if obstacles[ny*size + nx]:
				dx, dy = -dy, dx
				dxdy = 1<<(3*(dx+1)+dy)
			else:
				x, y = nx, ny
				xy = y*size + x
		return True

	x, y = start
	dx, dy = 0, -1
	pos_count = 1
	loop_count = 0
	xy = y*size + x
	dxdy = 1<<(3*(dx+1)+dy)
	seen = [0]*(size*size)

	while not (seen[xy] & dxdy):
		seen[xy] |= dxdy
		nx = x + dx
		ny = y + dy
		if not (0 <= nx < size and 0 <= ny < size): break
		if obstacles[ny*size + nx]:
			dx, dy = -dy, dx
			dxdy = 1<<(3*(dx+1)+dy)
		else:
			x, y = nx, ny
			xy = y*size + x
			if not seen[xy]:
				pos_count += 1
				obstacles[xy] = True
				loop_count += move(x-dx, y-dy, -dy, dx, seen.copy())
				obstacles[xy] = False

	print('Part 1:', pos_count)
	print('Part 2:', loop_count)

main()
