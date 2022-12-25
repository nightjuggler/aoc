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
	num_states = num_rows * num_cols // gcd(num_rows, num_cols)

	blizzards = [[] for i in range(4)]
	for y, row in enumerate(rows, start=1):
		for x, c in enumerate(row[1:-1]):
			if c != '.': blizzards['^v<>'.index(c)].append((x, y))

	start_xy, end_xy = (0, 0), (num_cols-1, num_rows+1)
	all_xy = {start_xy, end_xy}
	all_xy.update((x, y) for y in range(1, num_rows+1) for x in range(num_cols))
	states = [all_xy.difference(*blizzards)]
	states.extend(all_xy.difference(
			[(x, 1 + (y-1-i) % num_rows) for x, y in blizzards[0]],
			[(x, 1 + (y-1+i) % num_rows) for x, y in blizzards[1]],
			[((x-i) % num_cols, y) for x, y in blizzards[2]],
			[((x+i) % num_cols, y) for x, y in blizzards[3]])
			for i in range(1, num_states+1))
	assert states.pop() == states[0]
	return states, start_xy, end_xy

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
	states, start_xy, end_xy = read_input()
	steps = trip(states, start_xy, end_xy, 0)
	print('Part 1:', steps)
	steps = trip(states, end_xy, start_xy, steps)
	steps = trip(states, start_xy, end_xy, steps)
	print('Part 2:', steps)
main()
