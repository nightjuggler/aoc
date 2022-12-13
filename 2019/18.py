import argparse
from collections import deque
import sys

def connect(graph, loc, node):
	keys = 0
	q = deque()
	pq = deque()
	pq.append((loc, node))
	while pq:
		loc, node = pq.popleft()
		if loc in graph: continue
		graph[loc] = dest = []
		seen = set()
		q.append((0, node))
		while q:
			step, node = q.popleft()
			node_id, loc, adjacent = node
			if node_id in seen: continue
			seen.add(node_id)
			if loc and step:
				dest.append((loc & 63, step))
				pq.append((loc & 63, node))
				keys |= 1 << (loc & 31)
			else:
				q.extend((step + 1, node) for node in adjacent)
	return keys

def process(start):
	graph = {}
	all_keys = 0
	num_locs = len(start)
	assert 1 <= num_locs <= 4
	for i, node in enumerate(start):
		start[i] = loc = 27 + i
		all_keys |= connect(graph, loc, node)
	seen = {}
	best = None
	q = deque()
	q.append((0, sum(loc << i*6 for i, loc in enumerate(start)), 0))
	while q:
		step, locs, keys = q.popleft()
		state = (locs, keys)
		steps = seen.get(state)
		if steps is not None and steps <= step: continue
		seen[state] = step
		if best is not None and best <= step: continue
		for i in range(0, num_locs*6, 6):
			for dest, steps in graph[(locs >> i) & 63]:
				if not (dest & 32): # key
					dest_keys = keys | (1 << (dest & 31))
					if dest_keys == all_keys:
						if best is None or steps + step < best: best = steps + step
						continue
				elif keys & (1 << (dest & 31)): # door and have key
					dest_keys = keys
				else:
					continue
				q.append((steps + step, locs & ~(63 << i) | (dest << i), dest_keys))
	return best

def odd_gt3(n): return n > 3 and n & 1

def change_start(lines):
	assert odd_gt3(len(lines))
	line_len = len(lines[0])
	assert odd_gt3(line_len)
	assert all(len(line) == line_len for line in lines)
	y = len(lines) // 2
	x = line_len // 2
	for y, s_old, s_new in (
		(y-1, '...', '@#@'),
		(y  , '.@.', '###'),
		(y+1, '...', '@#@')
	):
		assert lines[y][x-1:x+2] == s_old
		lines[y] = lines[y][:x-1] + s_new + lines[y][x+2:]

def set_keys_and_doors(special):
	a_lower = ord('a')
	a_upper = ord('A')
	for i in range(26):
		key = chr(a_lower + i)
		door = chr(a_upper + i)
		key_node = special.pop(key, None)
		door_node = special.pop(door, None)
		if key_node:
			key_node[1] = 64 + i
			if not door_node:
				print(f"Key '{key}' has no door")
		if door_node:
			door_node[1] = 64 + 32 + i
			if not key_node:
				print(f"Door '{door}' has no key")
	assert not special

def parse_lines(lines):
	start = []
	node_id = 0
	special = {}
	curr_row = {}

	for line in lines:
		prev_row = curr_row
		curr_row = {}
		for x, c in enumerate(line):
			if c == '#': continue
			node_id += 1
			adjacent = []
			node = [node_id, 0, adjacent]
			if c != '.':
				if c == '@':
					start.append(node)
				else:
					assert c not in special
					special[c] = node
			if prev := prev_row.get(x):
				adjacent.append(prev)
				prev[2].append(node)
			if prev := curr_row.get(x-1):
				adjacent.append(prev)
				prev[2].append(node)
			curr_row[x] = node

	set_keys_and_doors(special)
	return start

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('part', nargs='?', type=int, choices=(1,2), default=1)
	args = parser.parse_args()

	lines = [line.rstrip() for line in sys.stdin]
	if args.part == 2:
		change_start(lines)

	print(f'Part {args.part}:', process(parse_lines(lines)))

if __name__ == '__main__':
	main()
