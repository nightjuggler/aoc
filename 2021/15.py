from collections import deque
import sys

def read_input():
	return [[int(c) for c in line.rstrip()] for line in sys.stdin]

def solve(grid):
	size = len(grid)
	assert all([len(row) == size for row in grid])
	print(size, 'x', size)

	best = [[-1] * size for row in grid]

	queues = [deque() for i in range(9)]
	queues[0].append((0, 0, 0))

	def process_queue():
		while True:
			for q in queues:
				if q: break
			else:
				return
			y, x, risk = q.popleft()

			if 0 <= best[y][x] <= risk:
				continue
			best[y][x] = risk

			for ay, ax in ((y,x+1), (y+1,x), (y,x-1), (y-1,x)):
				if ay < 0 or ay >= size: continue
				if ax < 0 or ax >= size: continue
				r = grid[ay][ax]
				queues[r-1].append((ay, ax, risk + r))

	full_size = size
	chunk_size = 10
	size = 0
	while size < full_size:
		for i in range(size):
			risk = best[i][size-1]
			r = grid[i][size]
			queues[r-1].append((i, size, risk + r))
			risk = best[size-1][i]
			r = grid[size][i]
			queues[r-1].append((size, i, risk + r))
		size = min(size + chunk_size, full_size)
		process_queue()

	return best[size-1][size-1]

def main():
	grid = read_input()
	if not grid:
		return

	print('Part 1:', solve(grid))

	d = len(grid)
	for row in grid:
		for i in range(1, 5):
			row.extend([x + 1 if x < 9 else 1 for x in row[-d:]])
	for i in range(1, 5):
		for row in grid[-d:]:
			grid.append([x + 1 if x < 9 else 1 for x in row])

	print('Part 2:', solve(grid))

if __name__ == '__main__':
	main()
