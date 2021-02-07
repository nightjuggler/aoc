import re
import sys

def err(message, *args):
	sys.exit(message.format(*args) if args else message)

def read_input(f):
	offset_pattern = '[-+][1-9][0-9]*'
	line_pattern = re.compile('[a-z]{{3}} (?:[ab](?:, {x})?|{x})$'.format(x=offset_pattern))
	code = []
	for i, line in enumerate(f, start=1):
		if not line_pattern.match(line):
			err('Line {} doesn\'t match pattern!', i)
		inst = line[:3]
		args = line[4:].rstrip()
		if inst in ('hlf', 'inc', 'tpl'):
			if args not in ('a', 'b'):
				err('Line {}: Invalid arguments!', i)
			args = (ord(args) - 97,)
		elif inst == 'jmp':
			if args[0] not in ('-', '+'):
				err('Line {}: Invalid arguments!', i)
			args = (int(args),)
		elif inst in ('jie', 'jio'):
			if args[1:3] != ', ':
				err('Line {}: Invalid arguments!', i)
			args = (ord(args[0]) - 97, int(args[3:]))
		else:
			err('Line {}: Unrecognized instruction!', i)
		code.append((inst, args))
	return code

def run(reg, code):
	n = len(code)
	i = 0
	while 0 <= i < n:
		inst, args = code[i]
		if inst == 'hlf':
			reg[args[0]] //= 2
			i += 1
		elif inst == 'inc':
			reg[args[0]] += 1
			i += 1
		elif inst == 'tpl':
			reg[args[0]] *= 3
			i += 1
		elif inst == 'jmp':
			i += args[0]
		elif inst == 'jie':
			if reg[args[0]] % 2 == 0:
				i += args[1]
			else:
				i += 1
		elif inst == 'jio':
			if reg[args[0]] == 1:
				i += args[1]
			else:
				i += 1
		else:
			err('Wtf?')

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-a', type=int, default=0)
	parser.add_argument('-b', type=int, default=0)
	args = parser.parse_args()

	code = read_input(sys.stdin)
	reg = [args.a, args.b]
	print(reg)
	run(reg, code)
	print(reg[1])

if __name__ == '__main__':
	main()
