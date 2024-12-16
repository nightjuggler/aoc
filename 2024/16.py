from collections import defaultdict, deque
import sys

def read_input():
	grid = [list(map('#.SE'.index, row.rstrip())) for row in sys.stdin]
	size = len(grid)
	assert size and all(len(row) == size for row in grid)
	assert not any(grid[0])
	assert not any(grid[-1])
	assert all(row[0] == 0 == row[-1] for row in grid)
	(st,sx,sy), (et,ex,ey) = sorted((tile, x, y)
		for y, row in enumerate(grid)
		for x, tile in enumerate(row) if tile >= 2)
	assert st == 2 and et == 3
	return grid, sx, sy, (ex, ey)

def main():
	grid, x, y, end = read_input()
	paths = defaultdict(set)
	best = None
	seen = {}
	q = deque()
	q.append((0, x, y, 1, 0, ((x, y),)))
	while q:
		score, x, y, dx, dy, path = q.popleft()
		if (x, y) == end:
			if best is None or score < best: best = score
			paths[score].update(path)
			continue
		key = x, y, dx, dy
		if key in seen and score > seen[key]: continue
		seen[key] = score
		q.append((score + 1000, x, y, dy, -dx, path)) # turn left
		q.append((score + 1000, x, y, -dy, dx, path)) # turn right
		x += dx
		y += dy
		if grid[y][x]:
			q.append((score + 1, x, y, dx, dy, path + ((x, y),)))
	print('Part 1:', best)
	print('Part 2:', len(paths[best]))

main()
