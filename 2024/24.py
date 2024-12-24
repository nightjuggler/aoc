import argparse
from collections import defaultdict, deque
import re
import sys

def op_and(a, b): return a & b
def op_or(a, b): return a | b
def op_xor(a, b): return a ^ b

def read_input(f):
	w = '([xyz][0-9]{2}|[a-w]{3})'
	pattern1 = re.compile(f'^{w}: (0|1)$')
	pattern2 = re.compile(f'^{w} (AND|OR|XOR) {w} -> {w}$')
	ready = {}
	for line_num, line in enumerate(f, start=1):
		if line == '\n': break
		if not (m := pattern1.match(line)):
			sys.exit(f'Line {line_num} doesn\'t match pattern!')
		wire, value = m.groups()
		ready[wire] = int(value)
	wires = defaultdict(list)
	for line_num, line in enumerate(f, start=line_num+1):
		if not (m := pattern2.match(line)):
			sys.exit(f'Line {line_num} doesn\'t match pattern!')
		in1, op, in2, out = m.groups()
		wires[in1].append((in2, op, out))
		wires[in2].append((in1, op, out))
	return ready, wires

def numbered_wires(wires, x):
	wires = sorted(wire for wire in wires if wire[0] == x)
	assert all(wire == f'{x}{i:02}' for i, wire in enumerate(wires))
	return wires

def part1(ready, wires):
	ops = {'AND': op_and, 'OR': op_or, 'XOR': op_xor}
	all_wires = set(ready)
	for wire1, gates in wires.items():
		all_wires.add(wire1)
		for wire2, op, wire3 in gates:
			all_wires.add(wire2)
			all_wires.add(wire3)
	q = deque()
	q.extend(ready)
	while q:
		wire1 = q.popleft()
		value1 = ready[wire1]
		for wire2, op, wire3 in wires[wire1]:
			if wire2 in ready:
				ready[wire3] = ops[op](value1, ready[wire2])
				q.append(wire3)
	assert set(ready) == all_wires
	zs = numbered_wires(ready, 'z')
	return sum(1<<i for i, wire in enumerate(zs) if ready[wire])

def part2(wires):
	wrong = set()

	def adder(wire, check_z=False):
		(in1, op1, out1), (in2, op2, out2) = wires[wire]
		if wire[0] == 'x':
			assert in1 == in2 == 'y' + wire[1:]
		if (op1, op2) != ('XOR', 'AND'):
			assert (op2, op1) == ('XOR', 'AND')
			out1, out2 = out2, out1
		if check_z:
			z = 'z' + check_z[1:]
			if out1 != z:
				wrong.add(out1)
				wrong.add(z)
			return out2
		return out1, out2

	xs = numbered_wires(wires, 'x')
	x = xs.pop(0)
	overflow1 = adder(x, x)

	for x in xs:
		xor, overflow2 = adder(x)

		if len(wires[xor]) != 2:
			wrong.add(xor)
			xor = overflow1

		overflow1 = adder(xor, x)

		gates = wires[overflow2]
		if len(gates) != 1:
			wrong.add(overflow2)
			gates = wires[overflow1]

		(in1, op1, overflow1), = gates
		assert op1 == 'OR'

	z = f'z{len(xs)+1:02}'
	if overflow1 != z:
		wrong.add(overflow1)
		wrong.add(z)

	return ','.join(sorted(wrong))

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('--part2', action='store_true')
	args = parser.parse_args()

	ready, wires = read_input(sys.stdin)
	print('Part 1:', part1(ready, wires))
	if args.part2:
		print('Part 2:', part2(wires))
main()
