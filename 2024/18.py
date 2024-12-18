import argparse
from heapq import heappop, heappush

def part1(blocked, max_xy):
	q = []
	heappush(q, (0, max_xy, max_xy))
	while q:
		steps, x, y = heappop(q)
		if not (x or y): return steps
		if blocked[y][x]: continue
		blocked[y][x] = True
		steps += 1
		if x: heappush(q, (steps, x-1, y))
		if y: heappush(q, (steps, x, y-1))
		if x < max_xy: heappush(q, (steps, x+1, y))
		if y < max_xy: heappush(q, (steps, x, y+1))
	return None

def part2(blocked, max_xy, remaining):
	size = max_xy + 1
	start = size*size - 1
	for bx, by in remaining:
		blocked[by][bx] = True
		seen = [False]*(start+1)
		q = []
		heappush(q, start)
		while q:
			xy = heappop(q)
			if not xy: break
			if seen[xy]: continue
			seen[xy] = True
			y, x = divmod(xy, size)
			if x and not blocked[y][x-1]: heappush(q, y*size + x-1)
			if y and not blocked[y-1][x]: heappush(q, (y-1)*size + x)
			if x < max_xy and not blocked[y][x+1]: heappush(q, y*size + x+1)
			if y < max_xy and not blocked[y+1][x]: heappush(q, (y+1)*size + x)
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

	print('Part 1:', part1([row.copy() for row in blocked], max_xy))
	print('Part 2:', part2(blocked, max_xy, coords[num_bytes:]))

main()
