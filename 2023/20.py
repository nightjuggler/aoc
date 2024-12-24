from collections import deque
import math
import re
import sys

def push_button(modules, states, conj, part1):
	q = deque()
	q.append(('button', False, 'broadcaster'))
	num_low = 0
	num_high = 0
	output_low = False
	while q:
		sender, pulse, receiver = q.popleft()
		if pulse:
			num_high += 1
		else:
			num_low += 1
		if receiver in conj:
			state = states[receiver]
			state[conj[receiver][sender]] = pulse
			pulse = not all(state)
		elif receiver in states:
			if pulse: continue # flip-flop modules ignore high pulses
			states[receiver] = pulse = not states[receiver]
		elif receiver != 'broadcaster':
			if not pulse: output_low = True
			continue
		q.extend((receiver, pulse, dest) for dest in modules[receiver])
	return (num_low, num_high) if part1 else output_low

def read_input():
	modules, states, conj, output = {}, {}, {}, None

	pattern = re.compile('^([%&]?[a-z]+) -> ([a-z]+(?:, [a-z]+)*)$')
	for linenum, line in enumerate(sys.stdin, start=1):
		if not (m := pattern.match(line)):
			sys.exit(f'Line {linenum} doesn\'t match pattern!')
		name, dests = m.groups()
		if name[0] == '&':
			name = name[1:]
			assert name != 'broadcaster'
			conj[name] = {}
			states[name] = []
		elif name[0] == '%':
			name = name[1:]
			assert name != 'broadcaster'
			states[name] = False
		else:
			assert name == 'broadcaster'
		dests = dests.split(', ')
		assert len(set(dests)) == len(dests)
		assert name not in modules
		modules[name] = dests

	for name, dests in modules.items():
		for dest in dests:
			if dest in conj:
				state = states[dest]
				conj[dest][name] = len(state)
				state.append(False)
			elif dest not in modules:
				assert dest in ('output', 'rx')
				if output:
					sys.exit('Cannot have more than one output!')
				output = dest, name

	return modules, states, conj, output

def part1(modules, states, conj):
	total_low = 0
	total_high = 0
	for _ in range(1000):
		num_low, num_high = push_button(modules, states, conj, True)
		total_low += num_low
		total_high += num_high
	return total_low * total_high

def split_input(modules):
	parts = []
	modules['rx'] = []
	for start in modules['broadcaster']:
		nodes = set()
		q = deque()
		q.append(start)
		while q:
			node = q.popleft()
			if node in nodes: continue
			nodes.add(node)
			q.extend(modules[node])
		nodes.remove('rx')
		parts.append((start, nodes))
	return parts

def part2(modules, states, conj, output):
	push_counts = []
	for node, nodes in split_input(modules):
		modules['broadcaster'] = [node]
		for node in nodes:
			states[node] = [False]*len(states[node]) if node in conj else False
		for node, i in conj[output].items():
			if node not in nodes: states[output][i] = True
		nodes = sorted(nodes)
		push_count = 0
		output_low = 0
		cache = {}
		while True:
			key = tuple(tuple(states[node]) if node in conj else states[node] for node in nodes)
			if key in cache: break
			cache[key] = push_count
			push_count += 1
			if push_button(modules, states, conj, False):
				assert not output_low
				output_low = push_count
		assert output_low and push_count-1 == output_low and cache[key] == 1
		push_counts.append(output_low)
	assert math.gcd(*push_counts) == 1
	return math.prod(push_counts)

def main():
	modules, states, conj, output = read_input()
	print('Part 1:', part1(modules, states, conj))
	if output and output[0] == 'rx':
		print('Part 2:', part2(modules, states, conj, output[1]))
main()
