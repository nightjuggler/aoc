import sys

def read_input():
	lines = [line.rstrip() for line in sys.stdin]
	num_lines = len(lines)

	if num_lines % 2 == 0 or any(len(line) != num_lines or line.strip('.#') for line in lines):
		sys.exit('The input is not valid!')

	return num_lines // 2, {(x, y) for y, line in enumerate(lines)
		for x, status in enumerate(line) if status == '#'}

def main():
	num_bursts = int(sys.argv[1]) if len(sys.argv) > 1 else 10_000
	y, infected = read_input()
	x = y
	dx, dy = 0, -1
	num_infected = 0

	for _ in range(num_bursts):
		node = x, y
		if node in infected:
			dx, dy = -dy, dx # right
			infected.remove(node)
		else:
			dx, dy = dy, -dx # left
			infected.add(node)
			num_infected += 1
		x += dx
		y += dy

	print(num_infected)

main()
