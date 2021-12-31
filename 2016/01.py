import re
import sys

def move(line, part1):
	facing = 0 # 0=north, 1=west, 2=south, 3=east
	pos = [0, 0]
	visited = set()

	for turn in line.split(', '):
		blocks = int(turn[1:])
		i = facing % 2
		if turn[0] == 'L':
			m = 1 if facing > 1 else -1
			facing = (facing + 1) % 4
		else:
			m = -1 if facing > 1 else 1
			facing = (facing + 3) % 4
		if part1:
			pos[i] += blocks * m
		else:
			for _ in range(blocks):
				pos[i] += m
				loc = tuple(pos)
				if loc in visited:
					return pos
				visited.add(loc)
	return pos if part1 else None

def main():
	turn_pattern = '[LR][1-9][0-9]*'
	line_pattern = re.compile(f'^{turn_pattern}(?:, {turn_pattern})*$')

	line = sys.stdin.readline()
	if not line_pattern.match(line):
		print("Input doesn't match expected pattern!")
		return

	def distance(pos): return sum(map(abs, pos)) if pos else pos

	print('Part 1:', distance(move(line, True)))
	print('Part 2:', distance(move(line, False)))

if __name__ == '__main__':
	main()
