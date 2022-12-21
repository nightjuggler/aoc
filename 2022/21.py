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

def get_rev(monkeys, name, rev_name):
	rev_monkeys = {name: 0}
	monkeys[name][1] = operator.sub

	def follow(name):
		if name == rev_name: return True
		args = monkeys[name]
		if isinstance(args, int): return False
		name1, op, name2 = args
		return follow(name1) or follow(name2)

	def invert():
		if op is operator.add: return [name, operator.sub, name2]
		if op is operator.sub: return [name2, operator.add if follow1 else op, name]
		if op is operator.mul: return [name, operator.floordiv, name2]
		return [name2, operator.mul if follow1 else op, name]

	while name != rev_name:
		name1, op, name2 = monkeys[name]
		follow1 = follow(name1)
		assert follow1 is not follow(name2)
		if not follow1: name1, name2 = name2, name1
		rev_monkeys[name1] = invert()
		rev_monkeys[name2] = get_num(monkeys, name2)
		name = name1

	return get_num(rev_monkeys, name)

def main():
	monkeys = read_input()
	print('Part 1:', get_num(monkeys, 'root'))
	print('Part 2:', get_rev(monkeys, 'root', 'humn'))
main()
