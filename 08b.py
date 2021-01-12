import sys
import re

def err(message, *args):
	sys.exit(message.format(*args))

def run(code):
	codelen = len(code)
	visited = [False] * codelen
	acc = 0
	i = 0
	while i < codelen:
		if visited[i]:
			return None
		visited[i] = True
		op, arg = code[i]
		if op == 'nop':
			i += 1
		elif op == 'acc':
			i += 1
			acc += arg
		elif op == 'jmp':
			i += arg
			if i < 0 or i > codelen:
				err('Invalid jump offset on line {}!', i+1)
		else:
			err('Invalid instruction on line {}!', i+1)
	return acc

def main():
	line_pattern = re.compile('^([a-z]{3}) ([-+](?:0|[1-9][0-9]*))$')
	code = []

	for line in sys.stdin:
		m = line_pattern.match(line)
		if not m:
			err('Line {} doesn\'t match pattern!', len(code) + 1)
		op, arg = m.groups()
		code.append([op, int(arg)])

	for i, instr in enumerate(code):
		op = instr[0]
		if op == 'nop':
			instr[0] = 'jmp'
		elif op == 'jmp':
			instr[0] = 'nop'
		else:
			continue
		acc = run(code)
		if acc is not None:
			print('Program terminates by changing {} to {} on line {}'.format(op, instr[0], i+1))
			print(acc)
		instr[0] = op

if __name__ == '__main__':
	main()
