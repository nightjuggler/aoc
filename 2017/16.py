import argparse
import sys

def do_dance(moves, size, reps):
	pos2prog = list(range(size))
	prog2pos = list(range(size))
	states = []
	for k in range(reps):
		states.append(pos2prog.copy())
		for move, i, j in moves:
			if move == 0:
				pos2prog = pos2prog[-i:] + pos2prog[:-i]
				for i, a in enumerate(pos2prog): prog2pos[a] = i
			elif move == 1:
				a, b = pos2prog[i], pos2prog[j]
				pos2prog[i], pos2prog[j] = b, a
				prog2pos[b], prog2pos[a] = i, j
			else:
				a, b = i, j
				i, j = prog2pos[a], prog2pos[b]
				pos2prog[i], pos2prog[j] = b, a
				prog2pos[b], prog2pos[a] = i, j
		if pos2prog == states[0]:
			pos2prog = states[reps % (k+1)]
			break
	return ''.join([chr(97 + a) for a in pos2prog])

def parse_dance(moves, size):
	dance = []
	for move in moves.strip().split(','):
		c = move[0]
		if c == 's':
			i = int(move[1:])
			assert 0 < i < size
			dance.append((0, i, None))
		elif c == 'x':
			i, j = map(int, move[1:].split('/'))
			assert 0 <= i < size
			assert 0 <= j < size
			dance.append((1, i, j))
		elif c == 'p':
			a, b = map(ord, move[1:].split('/'))
			a -= 97
			b -= 97
			assert 0 <= a < size
			assert 0 <= b < size
			dance.append((2, a, b))
		else:
			sys.exit('Unrecognized move!')
	return dance

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('--size', type=int, default=16)
	parser.add_argument('--reps', type=int, default=1_000_000_000)
	args = parser.parse_args()

	if (size := args.size) < 1: sys.exit('size must be >= 1!')
	if (reps := args.reps) < 1: sys.exit('reps must be >= 1!')

	dance = parse_dance(sys.stdin.readline(), size)
	print('Part 1:', do_dance(dance, size, 1))
	print('Part 2:', do_dance(dance, size, reps))
main()
