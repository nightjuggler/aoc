import argparse
from heapq import heappop, heappush

def part1(blocked, max_xy):
	size = max_xy + 1
	seen = [False]*(size*size)
	q = []
	heappush(q, (0, 0, 0))
	while q:
		steps, x, y = heappop(q)
		if x == max_xy == y: return steps
		key = y*size + x
		if seen[key]: continue
		seen[key] = True
		steps += 1
		if x and not blocked[y][x-1]: heappush(q, (steps, x-1, y))
		if y and not blocked[y-1][x]: heappush(q, (steps, x, y-1))
		if x < max_xy and not blocked[y][x+1]: heappush(q, (steps, x+1, y))
		if y < max_xy and not blocked[y+1][x]: heappush(q, (steps, x, y+1))
	return None

def part2(blocked, max_xy, remaining):
	size = max_xy + 1
	for bx, by in remaining:
		blocked[by][bx] = True
		seen = [False]*(size*size)
		q = []
		heappush(q, (0, 0, 0))
		while q:
			steps, x, y = heappop(q)
			if x == max_xy == y: break
			key = y*size + x
			if seen[key]: continue
			seen[key] = True
			steps += 1
			if x and not blocked[y][x-1]: heappush(q, (steps, x-1, y))
			if y and not blocked[y-1][x]: heappush(q, (steps, x, y-1))
			if x < max_xy and not blocked[y][x+1]: heappush(q, (steps, x+1, y))
			if y < max_xy and not blocked[y+1][x]: heappush(q, (steps, x, y+1))
		else:
			return f'{bx},{by}'
	return None

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('-x', '--example', action='store_true')
	args = parser.parse_args()

	max_xy, num_bytes, suffix = (6, 12, 'example') if args.example else (70, 1024, 'input')
	with open(f'data/18.{suffix}') as f:
		coords = [tuple(map(int, line.split(','))) for line in f]
	size = max_xy + 1
	blocked = [[False]*size for y in range(size)]
	for x, y in coords[:num_bytes]:
		blocked[y][x] = True

	print('Part 1:', part1(blocked, max_xy))
	print('Part 2:', part2(blocked, max_xy, coords[num_bytes:]))

main()
