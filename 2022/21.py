import operator
import re
import sys

def read_input():
	n = '[a-z]{4}'
	pattern = re.compile(f'{n}: (?:[1-9][0-9]*|(?:{n} [-+/*] {n}))$')
	ops = (operator.sub, operator.add, operator.floordiv, operator.mul)
	monkeys = {}
	for line_num, line in enumerate(sys.stdin, start=1):
		if not pattern.match(line):
			sys.exit(f'Line {line_num} doesn\'t match expected pattern!')
		monkey, *args = line.split()
		if len(args) == 1:
			args = int(args[0])
		else:
			args[1] = ops['-+/*'.index(args[1])]
		monkeys[monkey[:4]] = args
	return monkeys

def get_num(monkeys, name):
	args = monkeys[name]
	if isinstance(args, int): return args
	name1, op, name2 = args
	return op(get_num(monkeys, name1), get_num(monkeys, name2))

def uses_humn(monkeys, name):
	if name == 'humn': return True
	args = monkeys[name]
	if isinstance(args, int): return False
	name1, op, name2 = args
	return uses_humn(monkeys, name1) or uses_humn(monkeys, name2)

def make_rev(monkeys, rev_monkeys, name):
	if name == 'humn': return
	name1, op, name2 = monkeys[name]
	name1_uses_humn = uses_humn(monkeys, name1)
	name2_uses_humn = uses_humn(monkeys, name2)
	if name1_uses_humn:
		assert not name2_uses_humn
	else:
		assert name2_uses_humn
		name1, name2 = name2, name1
	if op is operator.add:
		rev_monkeys[name1] = [name, operator.sub, name2]
	elif op is operator.sub:
		if name1_uses_humn:
			rev_monkeys[name1] = [name, operator.add, name2]
		else:
			rev_monkeys[name1] = [name2, operator.sub, name]
	elif op is operator.mul:
		rev_monkeys[name1] = [name, operator.floordiv, name2]
	else:
		assert op is operator.floordiv
		if name1_uses_humn:
			rev_monkeys[name1] = [name, operator.mul, name2]
		else:
			rev_monkeys[name1] = [name2, operator.floordiv, name]
	rev_monkeys[name2] = get_num(monkeys, name2)
	make_rev(monkeys, rev_monkeys, name1)

def part2(monkeys):
	rev_monkeys = {}
	name1, op, name2 = monkeys['root']
	name1_uses_humn = uses_humn(monkeys, name1)
	name2_uses_humn = uses_humn(monkeys, name2)
	if name1_uses_humn:
		assert not name2_uses_humn
	else:
		assert name2_uses_humn
		name1, name2 = name2, name1
	rev_monkeys[name1] = get_num(monkeys, name2)
	make_rev(monkeys, rev_monkeys, name1)
	return get_num(rev_monkeys, 'humn')

def main():
	monkeys = read_input()
	print('Part 1:', get_num(monkeys, 'root'))
	print('Part 2:', part2(monkeys))
main()
