import sys

def move_knots(moves, num_knots):
	knots = [[0, 0] for _ in range(num_knots)]
	tail = knots[-1]
	head = knots.pop(0)
	tail_visited = {tuple(tail)}
	for d, n in moves:
		for _ in range(n):
			if   d == 0: head[1] -= 1 # up
			elif d == 1: head[1] += 1 # down
			elif d == 2: head[0] -= 1 # left
			else:        head[0] += 1 # right
			prev = head
			for knot in knots:
				dx = prev[0] - knot[0]
				dy = prev[1] - knot[1]
				ax = abs(dx)
				ay = abs(dy)
				if ax <= 1 and ay <= 1: break
				if dx: knot[0] += dx // ax
				if dy: knot[1] += dy // ay
				prev = knot
			else:
				tail_visited.add(tuple(tail))
	return len(tail_visited)

def main():
	moves = [('UDLR'.index(d), int(n)) for d, n in map(str.split, sys.stdin)]
	print('Part 1:', move_knots(moves, 2))
	print('Part 2:', move_knots(moves, 10))
main()
