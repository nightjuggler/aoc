from collections import defaultdict, deque
import re
import sys

class PuzzleError(Exception): pass

def err(message): raise PuzzleError(message)

def op_and(a, b): return a & b
def op_or(a, b): return a | b
def op_xor(a, b): return a ^ b

def read_input(f):
	w = '([xyz][0-9]{2}|[a-w]{3})'
	pattern1 = re.compile(f'^{w}: (0|1)$')
	pattern2 = re.compile(f'^{w} (AND|OR|XOR) {w} -> {w}$')
	ready = {}
	line_num = 0
	for line_num, line in enumerate(f, start=1):
		if line == '\n': break
		if not (m := pattern1.match(line)):
			err(f'Line {line_num} doesn\'t match pattern!')
		wire, value = m.groups()
		ready[wire] = int(value)
	wires = defaultdict(list)
	if not line_num:
		return ready, wires
	for line_num, line in enumerate(f, start=line_num+1):
		if not (m := pattern2.match(line)):
			err(f'Line {line_num} doesn\'t match pattern!')
		in1, op, in2, out = m.groups()
		wires[in1].append([in2, op, out])
		wires[in2].append([in1, op, out])
	return ready, wires

def numbered_wires(wires, x):
	wires = sorted(wire for wire in wires if wire[0] == x)
	if not all(wire == f'{x}{i:02}' for i, wire in enumerate(wires)):
		err(f'The wires beginning with {x} are not numbered correctly!')
	if not wires:
		err(f'There are no wires beginning with {x}!')
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
	if set(ready) != all_wires:
		err('Not all wires have a value!')
	zs = numbered_wires(ready, 'z')
	return sum(1<<i for i, wire in enumerate(zs) if ready[wire])

def part2(wires):
	wrong = set()
	lookup = defaultdict(list)
	for gates in wires.values():
		for gate in gates:
			lookup[gate[2]].append(gate)

	def fix(out1, out2):
		print('Swap', out1, 'with', out2)
		for gate in lookup[out1]: gate[2] = out2
		for gate in lookup[out2]: gate[2] = out1
		del lookup[out1]
		del lookup[out2]
		wrong.add(out1)
		wrong.add(out2)
		return out2

	def add(wire, check_z=False):
		def fail():
			err(f'Expected {wire} to be the input to one XOR and one AND gate with {wire2}!')
		wire2 = 'y' + wire[1:] if wire[0] == 'x' else overflow[2]
		if (len(wires[wire]) != 2 and (wire[0] == 'x' or not wires[wire2] or
			len(wires[wire := fix(wire, wires[wire2][0][0])]) != 2)): fail()
		g1, g2 = wires[wire]
		if not g1[0] == g2[0] == wire2: fail()
		if (g1[1], g2[1]) != ('XOR', 'AND'):
			g1, g2 = g2, g1
			if (g1[1], g2[1]) != ('XOR', 'AND'): fail()
		if check_z:
			z = 'z' + check_z[1:]
			if g1[2] != z: fix(g1[2], z)
			return g2
		return g1, g2

	def carry(wire):
		def fail():
			err(f'Expected {wire} to be the input to one OR gate with {wire2}!')
		wire2 = overflow[2]
		if (len(wires[wire]) != 1 and (not wires[wire2] or
			len(wires[wire := fix(wire, wires[wire2][0][0])]) != 1)): fail()
		g1, = wires[wire]
		if g1[0] != wire2 or g1[1] != 'OR': fail()
		return g1

	xs = numbered_wires(wires, 'x')
	x = xs.pop(0)
	overflow = add(x, x)

	for x in xs:
		xor, overflow2 = add(x)
		overflow = add(xor[2], x)
		overflow = carry(overflow2[2])

	z = f'z{len(xs)+1:02}'
	if overflow[2] != z: fix(overflow[2], z)

	return ','.join(sorted(wrong))

def main():
	try:
		ready, wires = read_input(sys.stdin)
	except PuzzleError as e:
		print(e)
		return
	try:
		result = part1(ready, wires)
	except PuzzleError as e:
		result = str(e)
	print('Part 1:', result)
	try:
		result = part2(wires)
	except PuzzleError as e:
		result = str(e)
	print('Part 2:', result)
main()
