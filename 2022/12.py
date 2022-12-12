from collections import deque
import sys

def search(grid, start, end):
	seen = set()
	q = deque()
	q.append((0, start, grid[start]))
	while q:
		step, xy, elev = q.popleft()
		if xy == end:
			return step
		if xy in seen:
			continue
		seen.add(xy)
		step += 1
		x, y = xy
		for xy in ((x+1, y), (x, y+1), (x-1, y), (x, y-1)):
			nelev = grid.get(xy)
			if nelev and nelev <= elev + 1:
				q.append((step, xy, nelev))
	return None

def main():
	grid = [row.strip() for row in sys.stdin]
	start = end = None
	for y, row in enumerate(grid):
		if (x := row.find('S')) >= 0:
			assert start is None
			start = x, y
		if (x := row.find('E')) >= 0:
			assert end is None
			end = x, y
	assert start is not None
	assert end is not None

	grid = {(x, y): ord(c) for y, row in enumerate(grid) for x, c in enumerate(row)}
	grid[start] = min_elev = ord('a')
	grid[end] = max_elev = ord('z')
	assert all(min_elev <= elev <= max_elev for elev in grid.values())

	print('Part 1:', search(grid, start, end))
	paths = [search(grid, xy, end) for xy, elev in grid.items() if elev == min_elev]
	paths = [steps for steps in paths if steps is not None]
	print('Part 2:', min(paths) if paths else None)
main()
