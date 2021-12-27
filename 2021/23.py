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
		if y1:
			grid[x1//2][y1-1] = 0
		else:
			grid[0][x1] = 0
		if y2:
			grid[x2//2][y2-1] = amp
		else:
			grid[0][x2] = amp
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

		room_size = len(grid[1])
		room_y = [0] * 5
		move_from_room = []

		for amp in range(1, 5):
			room = grid[amp]
			y = 0
			while y != room_size:
				if occupant := room[y]: break
				y += 1
			else:
				room_y[amp] = y
				continue
			if occupant == amp:
				y2 = y + 1
				while y2 != room_size:
					if room[y2] != amp: break
					y2 += 1
				else:
					room_y[amp] = y
					continue

			move_from_room.append((2*amp, y+1, occupant))

		for x, amp in enumerate(grid[0]):
			if y2 := room_y[amp]:
				try_move(energy, grid, amp, x, 0, 2*amp, y2)

		for x, y, amp in move_from_room:
			if ((y2 := room_y[amp]) and
				try_move(energy, grid, amp, x, y, 2*amp, y2)): continue
			for x2 in (0, 1, 3, 5, 7, 9, 10):
				try_move(energy, grid, amp, x, y, x2, 0)

		done = not (move_from_room or any(room_y))

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
	base = ord('A') - 1
	grid = [(0,) * 11]
	grid.extend([tuple([ord(letter) - base for letter in room]) for room in zip(*amphipods)])
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
