from collections import deque
import re
import sys

def read_input():
	n = '(?:[1-9][0-9]*|0)'
	pattern = re.compile(f'^{n} <-> {n}(?:, {n})*$')
	programs = {}
	for line_num, line in enumerate(sys.stdin, start=1):
		m = pattern.match(line)
		if not m:
			sys.exit(f'Line {line_num} doesn\'t match expected pattern!')
		p, plist = line.split(' <-> ')
		p = int(p)
		if p in programs:
			sys.exit(f'Line {line_num}: Duplicate record for {p}!')
		programs[p] = set(map(int, plist.split(', ')))
	for p1, plist in programs.items():
		for p in plist:
			if p not in programs:
				sys.exit(f'{p1} connects to {p}, but {p} has no record!')
			if p1 not in programs[p]:
				sys.exit(f'{p1} connects to {p}, but {p} doesn\'t connect to {p1}!')
	return programs

def group_size(p, programs):
	group = set()
	q = deque()
	q.append(p)
	while q:
		p = q.popleft()
		if p not in group:
			group.add(p)
			q.extend(programs[p])
	return len(group)

def count_groups(programs):
	q = deque()
	done = set()
	num_groups = 0
	for p in programs:
		if p in done: continue
		group = set()
		q.append(p)
		while q:
			p = q.popleft()
			if p not in group:
				group.add(p)
				q.extend(programs[p])
		done.update(group)
		num_groups += 1
	return num_groups

def main():
	programs = read_input()
	print('Part 1:', group_size(0, programs))
	print('Part 2:', count_groups(programs))

main()
