import sys

def part1(instrs):
	num_instrs = len(instrs)
	i = n = 0
	while i < num_instrs:
		offset = instrs[i]
		instrs[i] = offset + 1
		i += offset
		n += 1
	return n

def part2(instrs):
	num_instrs = len(instrs)
	i = n = 0
	while i < num_instrs:
		offset = instrs[i]
		instrs[i] = offset + (1 if offset < 3 else -1)
		i += offset
		n += 1
	return n

def main():
	instrs = list(map(int, sys.stdin))
	print('Part 1:', part1(instrs.copy()))
	print('Part 2:', part2(instrs))

if __name__ == '__main__':
	main()
