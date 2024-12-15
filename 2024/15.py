import sys

def read_input(f):
	grid = []
	for line in f:
		if line == '\n': break
		grid.append(list(map('.#O@'.index, line.rstrip())))
	size = len(grid)
	assert size and all(len(line) == size for line in grid)
	assert all(line[0] == 1 == line[-1] for line in grid)
	assert all(c == 1 for c in grid[0])
	assert all(c == 1 for c in grid[-1])
	bot = [(x, y) for y, line in enumerate(grid) for x, c in enumerate(line) if c == 3]
	assert len(bot) == 1
	dxdy = (0,-1), (1,0), (0,1), (-1,0)
	moves = []
	for line in f:
		moves.extend([dxdy['^>v<'.index(c)] for c in line.rstrip()])
	return grid, *bot[0], moves

def sum_gps(grid):
	return sum(100*y + x for y, row in enumerate(grid) for x, c in enumerate(row) if c == 2)

def part1(grid, x, y, moves):
	grid = [row.copy() for row in grid]
	for dx, dy in moves:
		x2 = x + dx
		y2 = y + dy
		boxes = 0
		while (c := grid[y2][x2]) == 2:
			x2 += dx
			y2 += dy
			boxes += 1
		if c: continue
		while boxes:
			grid[y2][x2] = 2
			x2 -= dx
			y2 -= dy
			boxes -= 1
		grid[y][x] = 0
		x, y = x2, y2
		grid[y][x] = 3
	return sum_gps(grid)

def print_grid(grid):
	for row in grid:
		print(''.join('.#[]@'[tile] for tile in row))

def widen_grid(grid):
	tilemap = (0,0), (1,1), (2,3), (4,0)
	for row in grid:
		new_row = []
		for tile in row:
			new_row.extend(tilemap[tile])
		row[:] = new_row

def move_x(grid, x, y, dx):
	row = grid[y]
	if dx > 0:
		x2 = x + 1
		while (tile := row[x2]) == 2: x2 += 2
		if tile: return False
		row[x+1:x2+1] = row[x:x2]
	else:
		x2 = x - 1
		while (tile := row[x2]) == 3: x2 -= 2
		if tile: return False
		row[x2:x] = row[x2+1:x+1]
	row[x] = 0
	return True

def move_y(grid, x, y, dy):
	boxes = {x}
	tomove = []
	while boxes:
		tomove.append(boxes)
		boxes = set()
		y += dy
		row = grid[y]
		for x in tomove[-1]:
			tile = row[x]
			if not tile: continue
			if tile == 1: return False
			boxes.add(x)
			boxes.add(x+1 if tile == 2 else x-1)
	for i in range(len(tomove)-1, -1, -1):
		row2 = row
		y -= dy
		row = grid[y]
		prev = tomove[i-1] if i else []
		for x in tomove[i]:
			row2[x] = row[x]
			if x not in prev: row[x] = 0
	return True

def part2(grid, x, y, moves):
	widen_grid(grid)
	x *= 2
	for dx, dy in moves:
		if dx:
			if move_x(grid, x, y, dx): x += dx
		else:
			if move_y(grid, x, y, dy): y += dy
	return sum_gps(grid)

def main():
	data = read_input(sys.stdin)
	print('Part 1:', part1(*data))
	print('Part 2:', part2(*data))
main()
