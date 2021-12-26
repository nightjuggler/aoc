import sys

def read_input():
	row_len = 0
	grid = []

	for line_number, line in enumerate(sys.stdin, start=1):
		row = []
		for c in line.rstrip():
			if c == '.':
				row.append(0)
			elif c == '>':
				row.append(1)
			elif c == 'v':
				row.append(2)
			else:
				print(f'Input line {line_number}: Unexpected character!')
				return None
		if row_len:
			if len(row) != row_len:
				print(f'Input line {line_number}: Unexpected length!')
				return None
		else:
			row_len = len(row)
			if row_len == 0:
				print(f'Input line {line_number} is empty!')
				return None
		grid.append(row)

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
