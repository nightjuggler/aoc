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
		row.insert(0, 9)
		row.append(9)
		grid.append(row)

	border = [9] * (line_length + 2)
	grid.insert(0, border)
	grid.append(border)
	return grid

def part2():
	grid = read_input()
	if not grid:
		return

	basin = 0
	basins = []
	yx2basin = {}
	width = len(grid[0]) - 1

	def mark_basin(d, y, x):
		yx = (y, x)
		b = yx2basin.get(yx)
		if b:
			if b != basin:
				print(f'Location {yx} in more than one basin?!')
			return 0
		yx2basin[yx] = basin
		size = 1
		for ay, ax in ((y-1, x), (y, x-1), (y, x+1), (y+1, x)):
			n = grid[ay][ax]
			if d <= n < 9:
				size += mark_basin(n, ay, ax)
		return size

	for y in range(1, len(grid) - 1):
		for x in range(1, width):
			d = grid[y][x]
			low_point = True
			for ay, ax in ((y-1, x), (y, x-1), (y, x+1), (y+1, x)):
				if d >= grid[ay][ax]:
					low_point = False
					break
			if low_point:
				basin += 1
				basins.append(mark_basin(d, y, x))

	if len(basins) < 3:
		print('There are fewer than 3 basins!')
		return

	basins.sort(reverse=True)
	print(basins[0] * basins[1] * basins[2])

def part1():
	risk = 0
	grid = [[int(d) for d in line.rstrip()] for line in sys.stdin]
	ymax = len(grid) - 1
	for y, row in enumerate(grid):
		xmax = len(row) - 1
		for x, d in enumerate(row):
			neighbors = []
			if y > 0: neighbors.append(grid[y-1][x])
			if x > 0: neighbors.append(grid[y][x-1])
			if y < ymax: neighbors.append(grid[y+1][x])
			if x < xmax: neighbors.append(grid[y][x+1])
			if all([d < n for n in neighbors]):
				risk += d + 1
	print(risk)

if __name__ == '__main__':
	if len(sys.argv) == 1:
		part1()
	elif len(sys.argv) != 2 or sys.argv[1] != '2':
		print('usage: wtf?')
	else:
		part2()
