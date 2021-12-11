import sys

def read_input():
	ord0 = ord('0')
	line_number = 0
	line_length = 0
	grid = []

	for line in sys.stdin:
		line_number += 1
		row = [ord(digit) - ord0 for digit in line.rstrip()]
		for digit in row:
			if digit < 0 or digit > 9:
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
		grid.append(row)

	return grid

def main(part1=True):
	grid = read_input()
	if not grid:
		return

	ymax = len(grid) - 1
	xmax = len(grid[0]) - 1
	flashes = 0

	def flash(y, x):
		nonlocal grid, ymax, xmax, flashes
		grid[y][x] = 0
		flashes += 1
		for dy in (-1, 0, 1):
			for dx in (-1, 0, 1):
				if dy == dx == 0: continue
				ay = y + dy
				ax = x + dx
				if ay < 0 or ay > ymax: continue
				if ax < 0 or ax > xmax: continue
				e = grid[ay][ax]
				if 0 < e < 10:
					e += 1
					grid[ay][ax] = e
					if e > 9:
						flash(ay, ax)

	def one_step():
		nonlocal grid
		grid = [[e + 1 for e in row] for row in grid]
		for y, row in enumerate(grid):
			for x, e in enumerate(row):
				if e > 9:
					flash(y, x)

	if part1:
		for step in range(100): one_step()
		print(flashes)
	else:
		size = len(grid) * len(grid[0])
		step = 0
		while flashes != size:
			flashes = 0
			one_step()
			step += 1
		print(step)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		main(part1=True)
	elif len(sys.argv) != 2 or sys.argv[1] != '2':
		print('usage: wtf?')
	else:
		main(part1=False)
