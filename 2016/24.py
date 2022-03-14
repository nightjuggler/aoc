from collections import deque
import sys

def read_input():
	numbers = {}
	locations = {}

	for y, line in enumerate(sys.stdin):
		for x, c in enumerate(line.rstrip()):
			if c == '#': continue
			locations[(x, y)] = 0
			if c == '.': continue
			n = ord(c) - ord('0')
			if not (0 <= n <= 9):
				sys.exit(f'Unexpected character at {(x, y)}!')
			if n in numbers:
				sys.exit(f'Duplicate occurrence of {n} at {numbers[n]} and {(x, y)}!')
			numbers[n] = (x, y)

	if not (numbers and len(numbers) == max(numbers) + 1):
		sys.exit('Please specify continuous integers starting with 0!')

	start_xy = numbers.pop(0)

	for n, xy in numbers.items():
		locations[xy] = 1 << (n - 1)

	return start_xy, locations, (1 << len(numbers)) - 1

def solve(start_xy, locations, numbers, part1):
	q = deque()
	q.append((0, *start_xy, 0))
	seen = {(*start_xy, 0)}

	while q:
		steps, x, y, visited = q.popleft()
		if visited == numbers and (part1 or (x, y) == start_xy): return steps
		steps += 1
		for xy in ((x+1, y), (x, y+1), (x-1, y), (x, y-1)):
			if (n := locations.get(xy)) is None: continue
			if (state := (*xy, visited | n)) in seen: continue
			q.append((steps, *state))
			seen.add(state)
	return None

def main():
	start_xy, locations, numbers = read_input()
	print('Part 1:', solve(start_xy, locations, numbers, True))
	print('Part 2:', solve(start_xy, locations, numbers, False))

if __name__ == '__main__':
	main()
