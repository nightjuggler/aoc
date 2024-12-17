import re

def init(puzzle_input):
	reg = '([1-9][0-9]*|0)'
	inst = '[0-7],[0-7]'

	m = re.fullmatch(
		f'Register A: {reg}\\n'
		f'Register B: {reg}\\n'
		f'Register C: {reg}\\n\\n'
		f'Program: ({inst}(?:,{inst})*)\\n',
		puzzle_input)

	*regs, prog = m.groups()
	regs = list(map(int, regs))
	prog = list(map(int, prog.split(',')))
	return regs, prog

def format_regs(regs):
	return f'A={regs[0]} B={regs[1]} C={regs[2]}'

def format_nums(label, nums):
	return f'{label}: {",".join(map(str, nums))}'

def run(regs, prog):
	def adv(arg): regs[0] >>= arg if arg < 4 else regs[arg-4]
	def bdv(arg): regs[1] = regs[0] >> (arg if arg < 4 else regs[arg-4])
	def cdv(arg): regs[2] = regs[0] >> (arg if arg < 4 else regs[arg-4])
	def bxl(arg): regs[1] ^= arg
	def bxc(arg): regs[1] ^= regs[2]
	def bst(arg): regs[1] = arg if arg < 4 else regs[arg-4] % 8
	def out(arg): output.append(arg if arg < 4 else regs[arg-4] % 8)

	code = adv, bxl, bst, None, bxc, out, bdv, cdv
	output = []
	n = len(prog)
	i = 0
	while i < n:
		op = prog[i]
		arg = prog[i+1]
		if op == 3:
			if regs[0]: i = arg; continue
		else:
			code[op](arg)
		i += 2
	return output

def part1(regs, prog):
	print('Part 1:', format_regs(regs), format_nums('Program', prog), '=>', end=' ')
	output = run(regs, prog)
	print(format_regs(regs), format_nums('Output', output))

def part2(prog):
	def adv(arg): return f'a >>= {arg if arg < 4 else "abc"[arg-4]}'
	def bdv(arg): return f'b = a >> {arg if arg < 4 else "abc"[arg-4]}'
	def cdv(arg): return f'c = a >> {arg if arg < 4 else "abc"[arg-4]}'
	def bxl(arg): return f'b ^= {arg}'
	def bxc(arg): return 'b ^= c'
	def bst(arg): return f'b = {arg}' if arg < 4 else f'b = {"abc"[arg-4]} % 8'

	assert prog[-2:] == [3,0] # Program must end with "jnz 0"
	assert not any(op == 3 for op in prog[:-2:2]) # Must not contain any other "jnz"
	assert prog[-4] == 5 # Second-to-last instruction must be "out"
	assert not any(op == 5 for op in prog[:-4:2]) # Must not contain any other "out"
	out = prog[-3]
	assert 4 <= out <= 6 # Must output register A, B, or C
	out = 'abc'[out-4]

	i = 2 * prog[::2].index(0) # Must contain one "adv" instruction
	a_shift = prog[i+1]
	assert 0 < a_shift < 4
	# The only instructions between the "adv" and "out" should be "bxl" or "bxc"
	assert all(op in (1, 4) for op in prog[i+2:-4:2])

	code = adv, bxl, bst, None, bxc, None, bdv, cdv
	source = [code[op](prog[2*i+1]) for i, op in enumerate(prog[:-4:2])]
	source = '\n\t\t\t\t'.join(source)
	exec_namespace = {}

	exec(f"""def solve(prog):
	start_a = 0
	for i in range(len(prog)-1, -1, -1):
		start_a <<= {a_shift}
		while True:
			a = start_a
			for x in prog[i:]:
				{source}
				if {out} % 8 != x: break
			else:
				break
			start_a += 1
	return start_a\n""", None, exec_namespace)

	a = exec_namespace['solve'](prog)
	assert run([a,0,0], prog) == prog
	print('Part 2:', a)

def main():
	print('==== Part 1 Inline Examples ====')
	for regs, prog in (
		([0,0,9], [2,6]),
		([10,0,0], [5,0,5,1,5,4]),
		([2024,0,0], [0,1,5,4,3,0]),
		([0,29,0], [1,7]),
		([0,2024,43690], [4,0]),
	):
		part1(regs, prog)

	print('==== Part 1 Example ====')
	with open('data/17.example1') as f:
		regs, prog = init(f.read())
	part1(regs, prog)

	print('==== Part 2 Example ====')
	with open('data/17.example2') as f:
		regs, prog = init(f.read())
	part2(prog)

	print('==== Puzzle Input ====')
	with open('data/17.input') as f:
		regs, prog = init(f.read())
	part1(regs, prog)
	part2(prog)

main()
