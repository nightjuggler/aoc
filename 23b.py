import sys

class Elem(object):
	def __init__(self, value):
		self.value = value

class LinkedList(object):
	def __init__(self):
		self.tail = None

	def append(self, value):
		tail = self.tail
		self.tail = elem = Elem(value)
		if tail is None:
			elem.next = elem
		else:
			elem.next = tail.next
			tail.next = elem
		return elem

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
	input_lookup = {
		'default': '463528179',
		'example': '389125467',
	}
	input_string = input_lookup.get(args[0], args[0]) if args else input_lookup['default']

	s = {}
	cups = LinkedList()
	for c in input_string:
		c = ord(c) - 48
		assert 1 <= c <= 9
		assert c not in s
		s[c] = cups.append(c)
	assert len(s) == 9
	for c in range(2, 10):
		s[c].dest = s[c - 1]
	d = s[9]
	for c in range(10, 1000001):
		e = cups.append(c)
		e.dest = d
		d = e
	s[1].dest = d

	h = cups.tail.next
#	for move in range(1, 101):
	for move in range(10000000):
#		print('move {}:'.format(move), llstr(h))

		d = h.dest
		x = h.next
		y = x.next
		z = y.next
		h.next = z.next
		h = h.next

		while d is x or d is y or d is z:
			d = d.dest

		z.next = d.next
		d.next = x

#	print('final:', llstr(h))

	while h.value != 1:
		h = h.next

#	print(llstr(h, sep='')[1:])

	x = h.next
	y = x.next
	x = x.value
	y = y.value
	print(x, '*', y, '=', x * y)

if __name__ == '__main__':
	main(sys.argv[1:])
