from collections import defaultdict
import sys

def main():
	tiles = [tuple(map(int, line.split(','))) for line in sys.stdin]
	num_tiles = len(tiles)
	areas = sorted(((
		(abs(tiles[i][0] - tiles[j][0]) + 1) *
		(abs(tiles[i][1] - tiles[j][1]) + 1), i, j)
		for i in range(num_tiles-1)
		for j in range(i+1, num_tiles)), reverse=True)
	print('Part 1:', areas[0][0])
	x1, y1 = tiles[-1]
	horz = defaultdict(list)
	vert = defaultdict(list)
	for x2, y2 in tiles:
		if y1 == y2:
			horz[y1].append(sorted((x1, x2)))
		else:
			assert x1 == x2
			vert[x1].append(sorted((y1, y2)))
		x1, y1 = x2, y2
	xs = {x: i for i, x in enumerate(sorted(vert))}
	ys = {y: i for i, y in enumerate(sorted(horz))}
	xn = len(xs)
	yn = len(ys)
	grid = [[False] * xn for y in range(yn)]
	for y, row in zip(ys, grid):
		for x1, x2 in horz[y]:
			x1 = xs[x1]
			x2 = xs[x2]
			row[x1:x2+1] = [True] * (x2+1-x1)
	for x, col in xs.items():
		for y1, y2 in vert[x]:
			y1 = ys[y1]
			y2 = ys[y2]
			for row in range(y1, y2+1):
				grid[row][col] = True
	for row in grid:
		inside = onside = False
		for x in range(xn):
			if row[x]:
				if not onside:
					inside = not inside
					onside = True
			else:
				if inside: row[x] = True
				onside = False
	for area, i, j in areas:
		x1, y1 = tiles[i]
		x2, y2 = tiles[j]
		if x1 > x2: x1,x2=x2,x1
		if y1 > y2: y1,y2=y2,y1
		y_range = range(ys[y1], ys[y2]+1)
		x_range = slice(xs[x1], xs[x2]+1)
		if all(all(grid[y][x_range]) for y in y_range):
			print('Part 2:', area)
			break
main()
