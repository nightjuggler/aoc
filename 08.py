import sys
import re

def err(message, *args):
	sys.exit(message.format(*args))

def run(code):
	codelen = len(code)
	acc = 0
	i = 0
	while i < codelen:
		instr = code[i]
		op, arg, visited = instr
		if visited:
			print(acc)
			break
		instr[2] = True
		if op == 'nop':
			i += 1
		elif op == 'acc':
			i += 1
			acc += arg
		elif op == 'jmp':
			i += arg
			if i < 0 or i > codelen:
				err('Invalid jump offset on line {}!', i)
		else:
			err('Invalid instruction on line {}!', i)

def main():
	line_pattern = re.compile('^([a-z]{3}) ([-+](?:0|[1-9][0-9]*))$')
	code = []

	for line in sys.stdin:
		m = line_pattern.match(line)
		if not m:
			err('Line {} doesn\'t match pattern!', len(code) + 1)
		op, arg = m.groups()
		code.append([op, int(arg), False])

	run(code)

if __name__ == '__main__':
	main()
