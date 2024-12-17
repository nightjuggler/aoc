from collections import defaultdict
from heapq import heappop, heappush
import sys

def read_input():
	grid = [list(map('#.SE'.index, row.rstrip())) for row in sys.stdin]
	size = len(grid)
	assert size and all(len(row) == size for row in grid)
	assert not any(grid[0])
	assert not any(grid[-1])
	assert all(row[0] == 0 == row[-1] for row in grid)
	assert grid[-2][1] == 2 # Start
	assert grid[1][-2] == 3 # End
	return grid

def main():
	grid = read_input()
	size = len(grid)
	x, y = 1, size-2
	end = size-2, 1
	paths = defaultdict(set)
	best = None
	seen = [1<<24]*(size*size*4)
	q = []
	heappush(q, (0, x, y, 1, 0, (y*size+x,)))
	while q:
		score, x, y, dx, dy, path = heappop(q)
		if (x, y) == end:
			paths[score].update(path)
			best = min(paths)
			continue
		if best and score >= best: continue
		key = (y*size+x)*4 + (3*(dx+1)+dy)//2
		if score > seen[key]: continue
		seen[key] = score
		heappush(q, (score + 1000, x, y, dy, -dx, path)) # turn left
		heappush(q, (score + 1000, x, y, -dy, dx, path)) # turn right
		x += dx
		y += dy
		if grid[y][x]:
			heappush(q, (score + 1, x, y, dx, dy, path + (y*size+x,)))
	print('Part 1:', best)
	print('Part 2:', len(paths[best]))

main()
