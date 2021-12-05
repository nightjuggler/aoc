import re
import sys

def read_input():
	line_pattern = re.compile('^([xy])=([1-9][0-9]*), ([xy])=([1-9][0-9]*)\\.\\.([1-9][0-9]*)$')
	line_number = 0
	xmin, xmax, ymin, ymax = None, None, None, None
	clay = set()

	for line in sys.stdin:
		line_number += 1
		m = line_pattern.match(line)
		if not m:
			print('Line', line_number, 'doesn\'t match pattern!')
			return
		n1, v1, n2, v2, v3 = m.groups()
		if n1 == n2:
			print('Line', line_number, 'doesn\'t match pattern!')
			return
		v1 = int(v1)
		v2 = int(v2)
		v3 = int(v3)
		if v2 > v3:
			print('Line', line_number, 'doesn\'t match pattern!')
			return
		if n1 == 'x':
			if line_number == 1:
				xmin = xmax = v1
				ymin, ymax = v2, v3
			else:
				if v1 < xmin: xmin = v1
				elif v1 > xmax: xmax = v1
				if v2 < ymin: ymin = v2
				if v3 > ymax: ymax = v3
			for y in range(v2, v3 + 1):
				clay.add((v1, y))
		else:
			if line_number == 1:
				ymin = ymax = v1
				xmin, xmax = v2, v3
			else:
				if v1 < ymin: ymin = v1
				elif v1 > ymax: ymax = v1
				if v2 < xmin: xmin = v2
				if v3 > xmax: xmax = v3
			for x in range(v2, v3 + 1):
				clay.add((x, v1))

	xmin -= 1
	xmax += 1
	w = xmax - xmin + 1
	h = ymax - ymin + 1
	print(f'w = {w}, h = {h}, w*h = {w*h}')
	print('len(clay) =', len(clay))

	grid = [[0] * w for y in range(h)]
	for x, y in clay:
		grid[y - ymin][x - xmin] = 1

	return grid, 500 - xmin

def print_grid(grid):
	tiles = ('.', '#', '|', '~')
	for row in grid:
		print(''.join([tiles[tile] for tile in row]))

def fill(grid, start_y, start_x):
	max_y = len(grid) - 1
	y = start_y

	while True:
		grid[y][start_x] = 2
		y += 1
		if y > max_y:
			return False
		tile = grid[y][start_x]
		if tile == 1:
			break
		if tile == 2:
			return False
		if tile == 3:
			break
	while True:
		y -= 1
		x = start_x
		left_blocked = 0
		while True:
			x -= 1
			tile = grid[y][x]
			if tile == 1:
				left_blocked = x
				break
			if tile == 2:
				break
			grid[y][x] = 2
			if grid[y + 1][x] == 0 and not fill(grid, y + 1, x):
				break
		x = start_x
		right_blocked = 0
		while True:
			x += 1
			tile = grid[y][x]
			if tile == 1:
				right_blocked = x
				break
			if tile == 2:
				break
			grid[y][x] = 2
			if grid[y + 1][x] == 0 and not fill(grid, y + 1, x):
				break

		if not (left_blocked and right_blocked):
			return False
		for x in range(left_blocked + 1, right_blocked):
			grid[y][x] = 3
		if y == start_y:
			break
	return True

def main():
	grid, spring_x = read_input()
	width = len(grid[0])

	if not (0 <= spring_x < width):
		print('The water will flow down unobstructed!')
		print(len(grid))
		print(0)
		return
	if grid[0][spring_x] != 0:
		print('The tile below the spring at the minimum y value must be sand!')
		return

	fill(grid, 0, spring_x)
#	print(''.join(['+' if x == spring_x else '.' for x in range(width)]))
#	print_grid(grid)

	water = 0
	water_at_rest = 0
	for row in grid:
		for tile in row:
			if tile > 1:
				water += 1
				if tile == 3:
					water_at_rest += 1
	print(water)
	print(water_at_rest)

if __name__ == '__main__':
	main()
