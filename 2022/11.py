import operator
import re
import sys

def err(line_num):
	sys.exit(f'Line {line_num} doesn\'t match expected pattern!')

class Monkey(object):
	pass

def play(monkeys, num_rounds, op2, op2_arg):
	activity = [0] * len(monkeys)
	for m in monkeys: m.items = list(m.start)
	monkeys = [(m.id, m.items, m.op, m.op_arg, m.divisor,
		(monkeys[m.false].items, monkeys[m.true].items)) for m in monkeys]

	for _ in range(num_rounds):
		for i, items, op, op_arg, divisor, items2 in monkeys:
			for worry in items:
				worry = op2(op(worry, op_arg or worry), op2_arg)
				items2[not worry % divisor].append(worry)
			activity[i] += len(items)
			items.clear()

	activity.sort(reverse=True)
	m1 = activity[0]
	m2 = activity[1]
	return f'{m1} * {m2} = {m1*m2}'

def read_input():
	n = '[1-9][0-9]*'
	patterns = (
		re.compile('^Monkey ([0-9]):$'),
		re.compile(f'^Starting items: ({n}(?:, {n})*)$'),
		re.compile(f'^Operation: new = old ([*+] (?:{n}|old))$'),
		re.compile(f'^Test: divisible by ({n})$'),
		re.compile('^If true: throw to monkey ([0-9])$'),
		re.compile('^If false: throw to monkey ([0-9])$'),
		None
	)
	attributes = ('id', 'start', 'op', 'divisor', 'true', 'false')
	expect = 0
	monkeys = []
	line_num = 0

	for line_num, line in enumerate(sys.stdin, start=1):
		line = line.strip()
		pattern = patterns[expect]
		if not pattern:
			if line: err(line_num)
			expect = 0
			continue
		m = pattern.match(line)
		if not m: err(line_num)
		if not expect:
			monkey = Monkey()
			monkeys.append(monkey)
		setattr(monkey, attributes[expect], m.group(1))
		expect += 1

	if patterns[expect]: err(line_num+1)
	return monkeys

def main():
	monkeys = read_input()

	mod = 1
	for i, m in enumerate(monkeys):
		m.id = int(m.id)
		m.start = tuple(map(int, m.start.split(', ')))
		m.true = int(m.true)
		m.false = int(m.false)
		m.divisor = int(m.divisor)
		mod *= m.divisor

		op, op_arg = m.op.split()
		m.op = operator.add if op == '+' else operator.mul
		m.op_arg = 0 if op_arg == 'old' else int(op_arg)

		assert i == m.id
		assert i != m.true < len(monkeys)
		assert i != m.false < len(monkeys)

	print('Part 1:', play(monkeys, 20, operator.floordiv, 3))
	print('Part 2:', play(monkeys, 10_000, operator.mod, mod))
main()
