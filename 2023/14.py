import sys

def solve(rocks, num_steps):
	seen = {}
	num_rows = len(rocks)

	for step in range(num_steps):
		rocks = list(map(list, zip(*map(reversed, rocks))))

		if step % 4 == 0:
			state = tuple(map(''.join, rocks))
			if state in seen:
				cycle_start = seen[state]
				last_step = cycle_start + (num_steps - cycle_start) % (step - cycle_start)
				for state, step in seen.items():
					if step == last_step:
						rocks = state
						break
				else:
					sys.exit(f'Step {last_step} not cached!')
				break
			seen[state] = step

		for row in rocks:
			i = 0
			for j, rock in enumerate(row):
				if rock == 'O':
					row[j] = '.'
					row[i] = 'O'
					i += 1
				elif rock == '#':
					i = j + 1

	for step in range(-step % 4):
		rocks = list(zip(*map(reversed, rocks)))

	return sum(sum(num_rows - y for y, rock in enumerate(row) if rock == 'O') for row in rocks)

def main():
	rocks = [line.rstrip()[::-1] for line in sys.stdin]
	print('Part 1:', solve(rocks, 1))
	print('Part 2:', solve(rocks, 1_000_000_000*4))
main()
