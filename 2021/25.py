import sys

def read_input():
	grid = []
	for line_num, line in enumerate(sys.stdin, start=1):
		try:
			grid.append(list(map('.>v'.index, line.rstrip())))
		except ValueError:
			sys.exit(f'Input line {line_num}: Unexpected character!')
		if not len(grid[0]) == len(grid[-1]) > 0:
			sys.exit(f'Input line {line_num}: Unexpected length!')
	return grid

def move(grid):
	y_len = len(grid)
	x_len = len(grid[0])
	moved = False
	new_grid = [row.copy() for row in grid]
	for row, new_row in zip(grid, new_grid):
		for x in range(x_len):
			if row[x] == 1:
				next_x = (x + 1) % x_len
				if row[next_x] == 0:
					new_row[x] = 0
					new_row[next_x] = 1
					moved = True
	grid = new_grid
	new_grid = [row.copy() for row in grid]
	for y, row in enumerate(grid):
		for x in range(x_len):
			if row[x] == 2:
				next_y = (y + 1) % y_len
				if grid[next_y][x] == 0:
					new_grid[y][x] = 0
					new_grid[next_y][x] = 2
					moved = True
	return moved, new_grid

def main():
	grid = read_input()
	if not grid: return

	step = 0
	while True:
		moved, grid = move(grid)
		step += 1
		if not moved:
			break
	print(step)

if __name__ == '__main__':
	main()
