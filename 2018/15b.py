import sys

def read_input():
	valid_chars = [ord(c) for c in '#.EG']
	line_number = 0
	line_length = 0
	grid = []

	for line in sys.stdin:
		line_number += 1
		row = [ord(c) for c in line.rstrip()]
		for c in row:
			if c not in valid_chars:
				print(f'Input line {line_number}: Unexpected character!')
				return None
		if line_length:
			if len(row) != line_length:
				print(f'Input line {line_number}: Unexpected length!')
				return None
		else:
			line_length = len(row)
			if line_length == 0:
				print(f'Input line {line_number} is empty!')
				return None
		grid.append(row)

	return grid

def print_grid(grid, yx2unit):
	elf, goblin = ord('E'), ord('G')
	for y, row in enumerate(grid):
		print(''.join([chr(c) for c in row]), ' ',
			', '.join([f'{chr(c)}({yx2unit[(y, x)][3]})'
				for x, c in enumerate(row) if c == elf or c == goblin]))
	print()

def get_move(d_grid, y, x, best, distance, step):
	moves = []
	for ay, ax in ((y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)):
		d = d_grid[ay][ax]
		if d == 0:
			candidate = (distance, (y, x), step)
			return candidate if not best or candidate < best else best
		if d and (not d[0] or distance + 1 < d[0]):
			moves.append((d, ay, ax))
	distance += 1
	if best and distance > best[0]:
		return best
	for d, ay, ax in moves:
		d[0] = distance
		d[1] = step or (ay, ax)
		best = get_move(d_grid, ay, ax, best, distance, d[1])
	return best

class ElfKilled(Exception):
	pass

def play(grid, elf_power, verbose):
	elf, goblin, empty = ord('E'), ord('G'), ord('.')
	elves, goblins, units = [], [], []
	yx2unit = {}

	for y, row in enumerate(grid):
		for x, c in enumerate(row):
			if c == elf:
				yx2unit[(y, x)] = unit = [y, x, c, 200]
				elves.append(unit)
				units.append(unit)
			elif c == goblin:
				yx2unit[(y, x)] = unit = [y, x, c, 200]
				goblins.append(unit)
				units.append(unit)

	def combat(y, x, opponents):
		nonlocal grid, empty, yx2unit, elf, elf_power
		opponent = opponents[0][2]
		target = None
		for yx in ((y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)):
			unit = yx2unit.get(yx)
			if unit and unit[2] == opponent and (not target or unit[3] < target[3]):
				target = unit
		if not target:
			return False
#		print(f'{chr(grid[y][x])} @ {y},{x} attacks {chr(opponent)} @ {target[0]},{target[1]}')
		target[3] -= 3 if opponent == elf else elf_power
		if target[3] <= 0:
			if opponent == elf:
				raise ElfKilled()
			y, x = target[0], target[1]
			grid[y][x] = empty
			del yx2unit[(y, x)]
			opponents.remove(target)
		return True

	def all_blocked(opponents):
		nonlocal grid, empty
		for unit in opponents:
			y, x = unit[0], unit[1]
			for ay, ax in ((y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)):
				if grid[ay][ax] == empty:
					return False
		return True

	rounds = 0
	if verbose:
		print('Initially:')
		print_grid(grid, yx2unit)
	while True:
		for unit in sorted(units):
			y, x, u, hp = unit
			if hp <= 0:
				continue
			opponents = goblins if u == elf else elves
			if not opponents:
				print('Game over!', 'Elves' if u == elf else 'Goblins', 'win!')
				hp = sum([unit[3] for unit in units if unit[3] > 0])
				print(rounds, '*', hp, '=', rounds * hp)
				return rounds * hp
			if combat(y, x, opponents) or all_blocked(opponents):
				continue
			opponent = opponents[0][2]
			d_grid = [[[0, None] if c == empty else 0 if c == opponent else None for c in row]
				for row in grid]
			move = get_move(d_grid, y, x, None, 0, None)
			if move:
				grid[y][x] = empty
				del yx2unit[(y, x)]
				unit[0], unit[1] = y, x = move[2]
				grid[y][x] = u
				yx2unit[(y, x)] = unit
				if move[0] == 1:
					combat(y, x, opponents)
		rounds += 1
		if verbose:
			print('After', rounds, 'rounds:')
			print_grid(grid, yx2unit)

def main():
	initial_grid = read_input()
	verbose = False
	min_power = 4
	max_power = 200
	answer = None

	while min_power <= max_power:
		power = (min_power + max_power) // 2
		print('Trying elf attack power =', power)
		grid = [row.copy() for row in initial_grid]
		elf_killed = False
		try:
			outcome = play(grid, power, verbose)
		except ElfKilled:
			elf_killed = True
		if elf_killed:
			min_power = power + 1
		else:
			max_power = power - 1
			answer = outcome

	print('The answer is', answer)

if __name__ == '__main__':
	main()
