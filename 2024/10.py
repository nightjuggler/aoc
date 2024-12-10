from collections import deque
import sys

def main():
	topo = [list(map(int, line.strip())) for line in sys.stdin]
	size = len(topo)
	assert size and all(len(row) == size for row in topo)

	start = [(x, y) for y, row in enumerate(topo) for x, h in enumerate(row) if not h]
	max_xy = size - 1
	sum1 = sum2 = 0
	q = deque()

	for x, y in start:
		peaks = set()
		q.append((x, y, 0))
		while q:
			x, y, h = q.popleft()
			if h == 9:
				peaks.add((x, y))
				sum2 += 1
				continue
			h += 1
			if x > 0 and topo[y][x-1] == h:
				q.append((x-1, y, h))
			if y > 0 and topo[y-1][x] == h:
				q.append((x, y-1, h))
			if x < max_xy and topo[y][x+1] == h:
				q.append((x+1, y, h))
			if y < max_xy and topo[y+1][x] == h:
				q.append((x, y+1, h))
		sum1 += len(peaks)

	print('Part 1:', sum1)
	print('Part 2:', sum2)
main()
