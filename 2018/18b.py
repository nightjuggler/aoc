import re
import sys

def read_input():
	line_len = 0
	grid = []

	for line_num, line in enumerate(sys.stdin, start=1):
		line = line.rstrip()
		if line.strip('.|#'):
			sys.exit(f'Input line {line_num}: Unexpected character(s)!')
		if line_len:
			if len(line) != line_len:
				sys.exit(f'Input line {line_num}: Unexpected length!')
		elif not (line_len := len(line)):
			sys.exit(f'Input line {line_num} is empty!')
		grid.append([0, *map(ord, line), 0])

	empty_line = [0] * (line_len + 2)
	grid.insert(0, empty_line)
	grid.append(empty_line)
	return grid

def play(grid):
	open_ground, trees, lumberyard = map(ord, '.|#')

	grid_len = len(grid) - 1
	line_len = len(grid[0]) - 1
	new_grid = [grid[0]]

	for y in range(1, grid_len):
		row = [0]
		for x in range(1, line_len):
			neighbors = [
				grid[y-1][x-1], grid[y-1][x], grid[y-1][x+1],
				grid[y][x-1], grid[y][x+1],
				grid[y+1][x-1], grid[y+1][x], grid[y+1][x+1],
			]
			c = grid[y][x]
			if c == open_ground:
				if neighbors.count(trees) >= 3:
					c = trees
			elif c == trees:
				if neighbors.count(lumberyard) >= 3:
					c = lumberyard
			elif c == lumberyard:
				if not (lumberyard in neighbors and trees in neighbors):
					c = open_ground
			row.append(c)
		row.append(0)
		new_grid.append(row)

	new_grid.append(grid[0])
	return new_grid

def print_grid(grid):
	for row in grid[1:-1]:
		print(''.join([chr(c) for c in row[1:-1]]))
	print()

def main():
	grid = read_input()
	cache = []
	cache_size = 30
	num_minutes = 1_000_000_000

	for minute in range(num_minutes):
		if len(cache) == cache_size:
			del cache[0]
		cache.append(grid)
		grid = play(grid)
		if grid in cache:
			cache_index = cache.index(grid)
			cycle = len(cache) - cache_index
			print(f'The grid after minute {minute} is the same as {cycle} minutes ago!')
			grid = cache[cache_index + (num_minutes - minute - 1) % cycle]
			break

	wooded, num_wooded = ord('|'), 0
	lumber, num_lumber = ord('#'), 0

	for row in grid:
		for c in row:
			if c == wooded: num_wooded += 1
			elif c == lumber: num_lumber += 1

	print(f'wooded acres ({num_wooded}) * lumberyards ({num_lumber}) = {num_wooded * num_lumber}')

if __name__ == '__main__':
	main()
