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

def fill_distance(d_grid, y, x, distance, step):
	distance += 1
	for ay, ax in ((y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)):
		d = d_grid[ay][ax]
		if d and (not d[0] or distance < d[0]):
			d[0] = distance
			d[1] = step or (ay, ax)
			fill_distance(d_grid, ay, ax, distance, d[1])

def main():
	grid = read_input()

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
		nonlocal grid, yx2unit, empty
		c = opponents[0][2]
		opp = None
		for ay, ax in ((y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)):
			if grid[ay][ax] == c:
				unit = yx2unit[(ay, ax)]
				if not opp or unit[3] < opp[3]:
					opp = unit
		if not opp:
			return False
#		print(f'{chr(grid[y][x])} @ {y},{x} attacks {chr(c)} @ {opp[0]},{opp[1]}')
		opp[3] -= 3
		if opp[3] <= 0:
			y, x = opp[:2]
			grid[y][x] = empty
			del yx2unit[(y, x)]
			opponents.remove(opp)
		return True

	def all_blocked(opponents):
		nonlocal grid, empty
		for opp in opponents:
			y, x = opp[:2]
			for ay, ax in ((y - 1, x), (y, x - 1), (y, x + 1), (y + 1, x)):
				if grid[ay][ax] == empty:
					return False
		return True

	rounds = 0
	print('Initially:')
	print_grid(grid, yx2unit)
	while True:
		dead = []
		for unit in sorted(units):
			y, x, u, hp = unit
			if hp <= 0:
				dead.append(unit)
				continue
			opponents = goblins if u == elf else elves
			if not opponents:
				print('Game over!')
				hp_sum = sum([unit[3] for unit in units if unit[3] > 0])
				print(rounds, '*', hp_sum, '=', rounds * hp_sum)
				return
			if combat(y, x, opponents):
				continue
			if all_blocked(opponents):
				continue
			d_grid = [[[0, None] if c == empty else None for c in row] for row in grid]
			fill_distance(d_grid, y, x, 0, None)
			d_min, step = None, None
			for opp in sorted(opponents):
				oy, ox = opp[:2]
				for ay, ax in ((oy - 1, ox), (oy, ox - 1), (oy, ox + 1), (oy + 1, ox)):
					d = d_grid[ay][ax]
					if d and d[0] and (not d_min or d[0] < d_min):
						d_min, step = d
			if step:
				ay, ax = step
				grid[y][x] = empty
				grid[ay][ax] = u
				del yx2unit[(y, x)]
				yx2unit[step] = unit
				unit[0] = ay
				unit[1] = ax
				if d_min == 1:
					combat(ay, ax, opponents)
		for unit in dead:
			units.remove(unit)
		rounds += 1
		print('After', rounds, 'rounds:')
		print_grid(grid, yx2unit)

if __name__ == '__main__':
	main()
