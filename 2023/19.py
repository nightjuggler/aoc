import re
import sys

def read_input():
	parts = []
	workflows = {}

	dst = '(?:A|R|[a-z]+)'
	num = '[1-9][0-9]*'
	pattern1 = re.compile(f'^([a-z]+){{((?:[xmas][<>]{num}:{dst},)+{dst})}}$')
	pattern2 = re.compile(f'^{{x=({num}),m=({num}),a=({num}),s=({num})}}$')

	def process1(groups):
		name, rules = groups
		rules = rules.split(',')
		for i in range(len(rules)-1):
			rule, dst = rules[i].split(':')
			rules[i] = 'xmas'.index(rule[0]), rule[1] == '<', int(rule[2:]), dst
		workflows[name] = rules

	def process2(groups):
		parts.append(tuple(map(int, groups)))

	pattern = pattern1
	process = process1
	for linenum, line in enumerate(sys.stdin, start=1):
		if m := pattern.match(line):
			process(m.groups())
		elif not line.strip():
			pattern = pattern2
			process = process2
		else:
			sys.exit(f'Input line {linenum} doesn\'t match pattern!')
	return parts, workflows

def part1(parts, workflows):
	result = 0
	for part in parts:
		name = 'in'
		while True:
			rules = workflows[name]
			for i, lt, num, dst in rules[:-1]:
				if (part[i] < num) if lt else (part[i] > num):
					name = dst
					break
			else:
				name = rules[-1]
			if name == 'A':
				result += sum(part)
				break
			if name == 'R':
				break
	return result

def part2(workflows):
	accept = []

	def recurse(name, xmas):
		if name == 'A':
			accept.append(xmas)
			return
		if name == 'R':
			return
		rules = workflows[name]
		for i, lt, num, dst in rules[:-1]:
			rmin, rmax = xmas[i]
			if lt:
				if num <= rmin: continue
				xmas[i] = rmin, min(rmax, num-1)
				recurse(dst, xmas.copy())
				xmas[i] = max(num, rmin), rmax
			else:
				if num >= rmax: continue
				xmas[i] = max(rmin, num+1), rmax
				recurse(dst, xmas.copy())
				xmas[i] = rmin, min(num, rmax)
		recurse(rules[-1], xmas.copy())

	recurse('in', [(1, 4000)]*4)
	result = 0
	for xmas in accept:
		combos = 1
		for rmin, rmax in xmas:
			combos *= rmax - rmin + 1
		result += combos
	return result

def main():
	parts, workflows = read_input()
	print('Part 1:', part1(parts, workflows))
	print('Part 2:', part2(workflows))
main()
