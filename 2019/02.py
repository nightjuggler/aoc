import sys

def run(program, noun, verb):
	program = program.copy()
	program[1] = noun
	program[2] = verb
	for i in range(0, len(program), 4):
		op = program[i]
		if op == 1:
			a, b, c = program[i+1:i+4]
			program[c] = program[a] + program[b]
		elif op == 2:
			a, b, c = program[i+1:i+4]
			program[c] = program[a] * program[b]
		elif op == 99:
			break
		else:
			print('Unknown opcode at position', i)
			break
	return program[0]

def part2(program):
	for noun in range(100):
		for verb in range(100):
			if run(program, noun, verb) == 19690720:
				return 100 * noun + verb
	return None

def main():
	program = [int(n) for n in sys.stdin.readline().split(',')]
	print('Part 1:', run(program, 12, 2))
	print('Part 2:', part2(program))

if __name__ == '__main__':
	main()
