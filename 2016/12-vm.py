import sys

# Usage: python3 12-vm.py < data/12.input

# >>> TIMEFMT="%*E seconds"
# >>> time python3 12-vm.py < data/12.input
# Part 1: 318007
# Part 2: 9227661
# 3.390 seconds

# Note: See zshmisc(1) for the zsh time command and zshparam(1) for TIMEFMT

def read_input():
	regs = tuple('abcd')
	code = []
	for i, line in enumerate(sys.stdin):
		op, *args = line.split()
		if op == 'cpy':
			x, y = args
			x = regs.index(x) if (x_reg := x in regs) else int(x)
			y = regs.index(y)
			code.append((0, x_reg, x, y))
		elif op == 'jnz':
			x, y = args
			x = regs.index(x) if (x_reg := x in regs) else int(x)
			y = i + int(y)
			code.append((1, x_reg, x, y))
		elif op == 'inc':
			x, = args
			code.append((2, False, regs.index(x), 1))
		elif op == 'dec':
			x, = args
			code.append((2, False, regs.index(x), -1))
		else:
			sys.exit(f'Unknown instruction on line {i+1}!')
	return code

def solve(code, c):
	regs = [0] * 4
	regs[2] = c

	i = 0
	while True:
		for op, x_reg, x, y in code[i:]:
			if op == 2:
				regs[x] += y
				continue
			if x_reg:
				x = regs[x]
			if op == 0:
				regs[y] = x
			elif x:
				i = y
				break
		else:
			break
	return regs[0]

def main():
	code = read_input()
	print('Part 1:', solve(code, 0))
	print('Part 2:', solve(code, 1))

if __name__ == '__main__':
	main()
