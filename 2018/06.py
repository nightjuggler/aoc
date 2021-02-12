import sys

def main():
	coords = []
	min_x = min_y = max_x = max_y = None
	for line in sys.stdin:
		x, y = map(int, line.split(', '))
		if min_x is None:
			min_x = max_x = x
			min_y = max_y = y
		else:
			if   x < min_x: min_x = x
			elif x > max_x: max_x = x
			if   y < min_y: min_y = y
			if   y > max_y: max_y = y
		coords.append((x, y))

	print(len(coords), 'locations')
	coords = [(x - min_x, y - min_y) for x, y in coords]
	max_x -= min_x
	max_y -= min_y
	max_d = max_x + max_y + 1
	stop_x = max_x + 1
	stop_y = max_y + 1
	grid = [[[None, max_d] for x in range(stop_x)] for y in range(stop_y)]

	for i, (cx, cy) in enumerate(coords):
		for y in range(stop_y):
			dy = abs(y - cy)
			for x in range(stop_x):
				d = dy + abs(x - cx)
				loc = grid[y][x]
				d_loc = loc[1]
				if d < d_loc:
					loc[0] = i
					loc[1] = d
				elif d == d_loc:
					loc[0] = None

	if len(coords) <= 26:
		for row in grid:
			print(''.join(['.' if i is None else chr(ord('A' if d == 0 else 'a') + i) for i, d in row]))

	areas = [0] * len(coords)
	for y in range(stop_y):
		for x in range(stop_x):
			i = grid[y][x][0]
			if i is not None:
				a = areas[i]
				if a is not None:
					areas[i] = None if x == 0 or y == 0 or x == max_x or y == max_y else a + 1

	max_area = max([a for a in areas if a is not None])

	if len(coords) <= 26:
		for i, a in enumerate(areas):
			print(chr(ord('A') + i), '=>', a)

	print('The maximum area that is not infinite is', max_area)

if __name__ == '__main__':
	main()
