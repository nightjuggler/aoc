from heapq import heappush, heappop
import sys

def read_input():
	return [[int(c) for c in line.rstrip()] for line in sys.stdin]

def solve(grid):
	size = len(grid)
	assert all([len(row) == size for row in grid])
	print(size, 'x', size)

	best = [[-1] * size for row in grid]
	q = []
	heappush(q, (0, 0, 0))

	def process_queue():
		while q:
			risk, y, x = heappop(q)

			if 0 <= best[y][x] <= risk: continue
			best[y][x] = risk

			for ay, ax in ((y,x+1), (y+1,x), (y,x-1), (y-1,x)):
				if ay < 0 or ay >= size: continue
				if ax < 0 or ax >= size: continue
				heappush(q, (risk + grid[ay][ax], ay, ax))

	full_size = size
	size = 0
	while size < full_size:
		for i in range(size):
			heappush(q, (best[i][size-1] + grid[i][size], i, size))
			heappush(q, (best[size-1][i] + grid[size][i], size, i))
		size = min(size + 10, full_size)
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
