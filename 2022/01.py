import sys

def main():
	elf = 0
	elves = []
	for line in sys.stdin:
		if line := line.strip():
			elf += int(line)
		else:
			elves.append(elf)
			elf = 0
	elves.append(elf)
	elves.sort(reverse=True)
	print('Part 1:', elves[0])
	print('Part 2:', sum(elves[:3]))

main()
