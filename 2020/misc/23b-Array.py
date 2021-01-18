import sys
import time

def main(args):
	part_one = False
	num_cups = 1000000
	num_moves = 10000000
	s = '463528179'

	for arg in args:
		if arg == '-1':
			part_one = True
			num_cups = 9
			num_moves = 100
		elif arg == '-x':
			s = '389125467'

	t1 = time.perf_counter()

	n = [0] * (num_cups + 1)
	h = p = int(s[0])
	for i in range(1, 9):
		n[p] = c = int(s[i])
		p = c
	for c in range(10, num_cups + 1):
		n[p] = c
		p = c
	n[p] = h

	def nstr(e, sep=' '):
		r = []
		for i in range(num_cups):
			r.append(e)
			e = n[e]
		return sep.join([str(e) for e in r])

	t2 = time.perf_counter()
	print('Init: {:.6f}s'.format(t2 - t1))
	t1 = time.perf_counter()

	for move in range(1, num_moves + 1):
		if part_one:
			print('move {}:'.format(move), nstr(h))

		x = n[h]
		y = n[x]
		z = n[y]

		d = num_cups if h == 1 else h - 1

		while d == x or d == y or d == z:
			d = num_cups if d == 1 else d - 1

		n[h] = n[z]
		n[z] = n[d]
		n[d] = x
		h = n[h]

	if part_one:
		print('final:', nstr(h))
		print(nstr(n[1], sep='')[:-1])
	else:
		x = n[1]
		y = n[x]
		print(x, '*', y, '=', x * y)

	t2 = time.perf_counter()
	print('Game: {:.6f}s'.format(t2 - t1))

if __name__ == '__main__':
	main(sys.argv[1:])
