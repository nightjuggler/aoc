import re
import sys

def err(line_num): sys.exit(f'Line {line_num} doesn\'t match expected pattern!')

def read_input():
	n = '[1-9][0-9]*'
	pattern = re.compile(f'^{n},{n}(?: -> {n},{n})+$')
	paths = []
	for line_num, line in enumerate(sys.stdin, start=1):
		if not pattern.match(line): err(line_num)
		paths.append([tuple(map(int, pair.split(','))) for pair in line.split(' -> ')])
	if not paths: err(1)
	return paths

def make_grid(paths):
	grid = set()
	for (x, y), *path in paths:
		for nx, ny in path:
			dx = nx - x
			dy = ny - y
			if dx:
				assert not dy
				grid.update((x, y) for x in range(x, nx, dx // abs(dx)))
				x = nx
			else:
				assert dy
				grid.update((x, y) for y in range(y, ny, dy // abs(dy)))
				y = ny
		grid.add((x, y))
	return grid

def fill(grid, max_y, part_one):
	while True:
		x = 500
		for y in range(1, max_y + 1):
			if   (x  , y) not in grid: continue
			elif (x-1, y) not in grid: x -= 1
			elif (x+1, y) not in grid: x += 1
			else: y -= 1; break
		else:
			if part_one: break
		grid.add((x, y))
		if not y: break

def main():
	paths = read_input()
	max_y = max(y for path in paths for x, y in path)
	grid = make_grid(paths)
	n = len(grid)
	fill(grid, max_y, True)
	print('Part 1:', len(grid) - n)
	fill(grid, max_y + 1, False)
	print('Part 2:', len(grid) - n)

main()
