import argparse
from collections import defaultdict

def read_grid(f):
	m = {tile: -i for i, tile in enumerate('#.ES')}
	grid = [[m[tile] for tile in row.rstrip()] for row in f]
	size = len(grid)
	assert size >= 4 and all(len(row) == size for row in grid)
	assert not any(grid[0])
	assert not any(grid[-1])
	assert not any(row[0] or row[-1] for row in grid)
	return grid

def get_path(grid):
	start, end = [(x, y) for y, row in enumerate(grid) for x, tile in enumerate(row) if tile < -1]
	step = 0
	path = []
	next_xy = [start]
	while next_xy:
		(x, y), = next_xy
		next_xy = [(nx, ny) for nx, ny in ((x-1,y), (x,y-1), (x+1,y), (x,y+1)) if grid[ny][nx] < 0]
		grid[y][x] = step = step + 1
		path.append((x, y))
	assert (x, y) == end
	assert all(tile >= 0 for row in grid for tile in row)
	return path

def solve(path, grid, max_cheat, min_saved, verbose):
	size = len(grid)
	cheats = defaultdict(int)
	for step, (x, y) in enumerate(path, start=1):
		x_range = range(max(1, x-max_cheat), min(size, x+max_cheat+1))
		y_range = range(max(1, y-max_cheat), min(size, y+max_cheat+1))
		for y2 in y_range:
			for x2 in x_range:
				cheat_len = abs(y-y2) + abs(x-x2)
				if cheat_len <= max_cheat:
					saved = grid[y2][x2] - step - cheat_len
					if saved >= min_saved:
						cheats[saved] += 1
	if verbose:
		for saved, count in sorted(cheats.items()):
			print(f'There are {count} cheats that save {saved} picoseconds.')
	return sum(cheats.values())

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('-x', '--example', action='store_true')
	parser.add_argument('-v', '--verbose', action='store_true')
	args = parser.parse_args()

	filename, save1, save2 = ('example', 1, 50) if args.example else ('input', 100, 100)

	with open(f'data/20.{filename}') as f:
		grid = read_grid(f)

	path = get_path(grid)
	print('Part 1:', solve(path, grid, 2, save1, args.verbose))
	print('Part 2:', solve(path, grid, 20, save2, args.verbose))
main()
