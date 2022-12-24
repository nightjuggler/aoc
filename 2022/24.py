from collections import deque
import sys

def gcd(a, b):
	while b:
		a, b = b, a % b
	return a

def read_input():
	rows = list(map(str.rstrip, sys.stdin))
	assert len(rows) > 2
	row_len = len(rows[0])
	assert all(len(row) == row_len for row in rows)
	row = rows[0]
	assert row[:3] == '#.#' and not row[3:].strip('#')
	row = rows[-1]
	assert row[-3:] == '#.#' and not row[:-3].strip('#')
	rows = rows[1:-1]
	assert all(row[:1] == '#' == row[-1:] and not row[1:-1].strip('.^v<>') for row in rows)
	col = ''.join([row[1] for row in rows])
	assert not col.strip('.<>')
	col = ''.join([row[-2] for row in rows])
	assert not col.strip('.<>')

	num_rows = len(rows)
	num_cols = row_len - 2
	d = gcd(num_rows, num_cols)
	num_states = num_rows * num_cols // d

	start_xy = 0, 0
	end_xy = num_cols - 1, num_rows + 1
	clear = {start_xy, end_xy}
	blizzard_lists = [[] for i in range(4)]
	for y, row in enumerate(rows, start=1):
		for x, c in enumerate(row[1:-1]):
			if c == '.':
				clear.add((x, y))
			else:
				blizzard_lists['^v<>'.index(c)].append((x, y))
	dxdy = ((0,-1),(0,1),(-1,0),(1,0))
	states = [clear]
	while True:
		blizzard_lists = [[((x + dx) % num_cols, 1 + (y - 1 + dy) % num_rows) for x, y in blizzard_list]
			for blizzard_list, (dx, dy) in zip(blizzard_lists, dxdy)]
		blizzards = set()
		blizzards.update(*blizzard_lists)
		clear = {start_xy, end_xy}
		clear.update((x, y)
			for y in range(1, num_rows + 1)
				for x in range(num_cols)
					if (x, y) not in blizzards)
		if clear == states[0]: break
		states.append(clear)
	assert len(states) == num_states
	return states, end_xy

def trip(states, start_xy, end_xy, step):
	num_states = len(states)
	q = deque()
	q.append((step, start_xy))
	seen = set()
	best = None
	while q:
		step, xy = q.popleft()
		if xy == end_xy:
			if best is None or step < best: best = step
			continue
		if best and step >= best: continue
		x, y = xy
		state = (step % num_states, x, y)
		if state in seen: continue
		seen.add(state)
		step += 1
		clear = states[step % num_states]
		q.extend((step, xy) for xy in ((x+1,y), (x,y+1), (x-1,y), (x,y-1), (x,y)) if xy in clear)
	return best

def main():
	states, end_xy = read_input()
	steps = trip(states, (0, 0), end_xy, 0)
	print('Part 1:', steps)
	steps = trip(states, end_xy, (0, 0), steps)
	steps = trip(states, (0, 0), end_xy, steps)
	print('Part 2:', steps)
main()
