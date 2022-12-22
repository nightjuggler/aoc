import operator
import re
import sys

ops = (operator.sub, operator.add, operator.floordiv, operator.mul)

def read_input():
	n = '[a-z]{4}'
	pattern = re.compile(f'{n}: (?:[1-9][0-9]*|(?:{n} [-+/*] {n}))$')
	monkeys = {}
	for line_num, line in enumerate(sys.stdin, start=1):
		if not pattern.match(line):
			sys.exit(f'Line {line_num} doesn\'t match expected pattern!')
		monkey, *args = line.split()
		if len(args) == 1:
			args = int(args[0])
		else:
			args[1] = '-+/*'.index(args[1])
		monkeys[monkey[:4]] = args
	return monkeys

def get_num(monkeys, name):
	args = monkeys[name]
	if isinstance(args, int): return args
	name1, op, name2 = args
	return ops[op](get_num(monkeys, name1), get_num(monkeys, name2))

def get_rev(monkeys, name, rev_name):
	rev_monkeys = {name: 0}
	monkeys[name][1] = 0

	def follow(name):
		if name == rev_name: return True
		args = monkeys[name]
		if isinstance(args, int): return False
		name1, op, name2 = args
		if follow(name1):
			assert not follow(name2)
			rev_op = (1, 0, 3, 2)[op]
		elif follow(name2):
			name1, name2 = name2, name1
			rev_op = (0, 0, 2, 2)[op]
		else:
			return False
		rev_monkeys[name1] = [name, rev_op, name2] if op % 2 else [name2, rev_op, name]
		rev_monkeys[name2] = get_num(monkeys, name2)
		return True

	return get_num(rev_monkeys, rev_name) if follow(name) else None

def main():
	monkeys = read_input()
	print('Part 1:', get_num(monkeys, 'root'))
	print('Part 2:', get_rev(monkeys, 'root', 'humn'))
main()
