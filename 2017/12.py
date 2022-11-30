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

def remove_group(programs, p):
	todo = {p}
	size = 0
	while todo:
		if (p := todo.pop()) in programs:
			size += 1
			todo.update(programs.pop(p))
	return size

def count_groups(programs):
	num_groups = 0
	while programs:
		num_groups += 1
		p, todo = programs.popitem()
		while todo:
			if (p := todo.pop()) in programs:
				todo.update(programs.pop(p))
	return num_groups

def main():
	programs = read_input()
	print('Part 1:', remove_group(programs, 0))
	print('Part 2:', count_groups(programs) + 1)

main()
