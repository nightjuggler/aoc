import re
import sys

def read_input():
	valid_chars = [ord(c) for c in '.|#']
	line_number = 0
	line_length = 0
	grid = []

	for line in sys.stdin:
		line_number += 1
		row = [ord(c) for c in line.rstrip()]
		for c in row:
			if c not in valid_chars:
				print(f'Input line {line_number}: Unexpected character!')
				return None
		if line_length:
			if len(row) != line_length:
				print(f'Input line {line_number}: Unexpected length!')
				return None
		else:
			line_length = len(row)
			if line_length == 0:
				print(f'Input line {line_number} is empty!')
				return None
		row.insert(0, 0)
		row.append(0)
		grid.append(row)

	empty_line = [0] * (line_length + 2)
	grid.insert(0, empty_line)
	grid.append(empty_line)
	return grid

def play(grid):
	open_ground, trees, lumberyard = [ord(c) for c in '.|#']

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

	print_grid(grid)
	for minute in range(10):
		grid = play(grid)
		print_grid(grid)

	wooded, num_wooded = ord('|'), 0
	lumber, num_lumber = ord('#'), 0

	for row in grid[1:-1]:
		for c in row[1:-1]:
			if c == wooded: num_wooded += 1
			elif c == lumber: num_lumber += 1

	print(f'wooded acres ({num_wooded}) * lumberyards ({num_lumber}) = {num_wooded * num_lumber}')

if __name__ == '__main__':
	main()
