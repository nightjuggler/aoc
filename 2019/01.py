import sys

def main():
	module_masses = [int(m) for m in sys.stdin]

	print('Part 1:', sum([m // 3 - 2 for m in module_masses]))

	fuel = 0
	for m in module_masses:
		while (m := m // 3 - 2) > 0:
			fuel += m

	print('Part 2:', fuel)

main()
