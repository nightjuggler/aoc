import sys
import time

class Elem(object):
	def __init__(self, value, prev):
		self.value = value
		if prev:
			self.next = prev.next
			prev.next = self
		else:
			self.next = self

def llstr(head, sep=' '):
	values = []
	elem = head
	while True:
		values.append(elem.value)
		elem = elem.next
		if elem is head:
			break
	return sep.join([str(value) for value in values])

def main(args):
	part_one = False
	num_cups = 1000000
	num_moves = 10000000
	input_string = '463528179'

	for arg in args:
		if arg == '-1':
			part_one = True
			num_cups = 9
			num_moves = 100
		elif arg == '-x':
			input_string = '389125467'

	t1 = time.perf_counter()

	s = {}
	h = None
	for c in input_string:
		c = ord(c) - 48
		assert 1 <= c <= 9
		assert c not in s
		s[c] = h = Elem(c, h)
	assert len(s) == 9

	d = s[1]
	for c in range(2, 10):
		e = s[c]
		e.dest = d
		d = e
	for c in range(10, num_cups + 1):
		h = Elem(c, h)
		h.dest = d
		d = h
	s[1].dest = d

	t2 = time.perf_counter()
	print('Init: {:.6f}s'.format(t2 - t1))
	t1 = time.perf_counter()

	h = h.next
	for move in range(1, num_moves + 1):
		if part_one:
			print('move {}:'.format(move), llstr(h))

		x = h.next
		y = x.next
		z = y.next

		d = h.dest
		while d is x or d is y or d is z:
			d = d.dest

		h.next = z.next
		z.next = d.next
		d.next = x
		h = h.next

	if part_one:
		print('final:', llstr(h))

	while h.value != 1:
		h = h.next

	if part_one:
		print(llstr(h, sep='')[1:])
	else:
		x = h.next
		y = x.next
		x = x.value
		y = y.value
		print(x, '*', y, '=', x * y)

	t2 = time.perf_counter()
	print('Game: {:.6f}s'.format(t2 - t1))

if __name__ == '__main__':
	main(sys.argv[1:])
