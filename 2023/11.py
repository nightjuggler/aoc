import sys

def expand(delta, coords):
	num_empty = 0
	coord_map = {}
	prev_coord = -1
	for coord in sorted(set(coords)):
		num_empty += coord - prev_coord - 1
		coord_map[coord] = coord + num_empty * delta
		prev_coord = coord
	return coord_map

def solve(galaxies, expansion):
	xmap = expand(expansion-1, (x for x, y in galaxies))
	ymap = expand(expansion-1, (y for x, y in galaxies))

	galaxies = [(xmap[x], ymap[y]) for x, y in galaxies]

	return sum(abs(x2-x1) + abs(y2-y1)
		for i, (x1, y1) in enumerate(galaxies)
		for x2, y2 in galaxies[i+1:])

def main():
	galaxies = {(x, y) for y, line in enumerate(sys.stdin)
		for x, c in enumerate(line) if c == '#'}
	if len(sys.argv) > 1:
		print(solve(galaxies, int(sys.argv[1])))
	else:
		print('Part 1:', solve(galaxies, 2))
		print('Part 2:', solve(galaxies, 1_000_000))
main()
