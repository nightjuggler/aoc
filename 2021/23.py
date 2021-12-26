from heapq import heappush, heappop
import sys

def process_queue(q):
	best_energy = None
	state_cache = {}

	def try_move(energy, grid, amp, x1, y1, x2, y2):
		dx = x2 - x1
		steps = abs(dx)
		dx //= steps
		steps += y1 + y2

		hallway = grid[0]
		x = x1
		while x != x2:
			x += dx
			if hallway[x]:
				return False

		grid = [list(row) for row in grid]
		grid[y1][x1] = 0
		grid[y2][x2] = amp
		grid = tuple([tuple(row) for row in grid])

		heappush(q, (energy + steps * 10**(amp-1), grid))
		return True

	while q:
		energy, grid = heappop(q)

		if best_energy is not None and energy >= best_energy:
			continue

		cached_energy = state_cache.get(grid)
		if cached_energy is not None and energy >= cached_energy:
			continue
		state_cache[grid] = energy

		done = True
		gridlen = len(grid)
		amphipods = [(x, y, amp) for y, row in enumerate(grid)
			for x, amp in enumerate(row) if amp]

		for x, y, amp in amphipods:
			room_x = 2 * amp
			if x != room_x:
				done = False
			if y and grid[y-1][x]:
				continue
			if x == room_x:
				if all([grid[i][x] == amp for i in range(y+1, gridlen)]):
					continue
			else:
				for i in range(gridlen-1, 0, -1):
					if (occupant := grid[i][room_x]) != amp: break

				if not occupant and try_move(energy, grid, amp, x, y, room_x, i):
					continue
			if y:
				for x2 in (0, 1, 3, 5, 7, 9, 10):
					try_move(energy, grid, amp, x, y, x2, 0)

		if done and (best_energy is None or energy < best_energy):
			best_energy = energy

	return best_energy

def read_input():
	f = sys.stdin
	f.readline()
	f.readline()
	amphipods = []

	for i in range(2):
		line = f.readline().strip().replace('#', '')
		if len(line) != 4 or not all([c in 'ABCD' for c in line]):
			print(f'Input line {3+i} doesn\'t match pattern!')
			return None
		amphipods.append(line)

	return amphipods

def make_grid(amphipods):
	grid = [(0,) * 11]
	for amps in amphipods:
		row = [0] * 11
		for i, letter in enumerate(amps, start=1):
			row[2*i] = ord(letter) - ord('A') + 1
		grid.append(tuple(row))
	return tuple(grid)

def main():
	amphipods = read_input()
	if not amphipods: return

	q = []
	heappush(q, (0, make_grid(amphipods)))
	print('Part 1:', process_queue(q))

	amphipods[1:1] = 'DCBA', 'DBAC'
	heappush(q, (0, make_grid(amphipods)))
	print('Part 2:', process_queue(q))

if __name__ == '__main__':
	main()
