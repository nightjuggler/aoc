import sys

class ParseError(Exception):
	def __init__(self, s, i, c):
		super().__init__(f'Failed to parse "{s}": Expected a {c} in column {i+1}!')

class Node(object):
	def __init__(self, parent, value=None):
		self.left = None
		self.right = None
		self.value = value
		self.parent = parent

	def __str__(self):
		if self.value is not None:
			return str(self.value)
		return ''.join(('[', str(self.left), ',', str(self.right), ']'))

	def __abs__(self):
		if self.value is not None:
			return self.value
		return 3 * abs(self.left) + 2 * abs(self.right)

def parse(line, i, parent, depth=0):
	node = Node(parent)
	max_i = len(line) - 1

	def child():
		if depth == 4:
			if i > max_i or line[i] not in '0123456789':
				raise ParseError(line, i, 'digit')
		else:
			if i > max_i or line[i] not in '0123456789[':
				raise ParseError(line, i, 'digit or left bracket')
			if line[i] == '[':
				return parse(line, i, node, depth+1)

		return i, Node(node, int(line[i]))

	if i > max_i or line[i] != '[':
		raise ParseError(line, i, 'left bracket')
	i += 1
	i, node.left = child()
	i += 1
	if i > max_i or line[i] != ',':
		raise ParseError(line, i, 'comma')
	i += 1
	i, node.right = child()
	i += 1
	if i > max_i or line[i] != ']':
		raise ParseError(line, i, 'right bracket')
	return i, node

def read_input():
	numbers = []
	for line_number, line in enumerate(sys.stdin, start=1):
		line = line.rstrip()
		for c in line:
			if c not in ',0123456789[]':
				print(f'Unexpected character on input line {line_number}!')
				return None
		numbers.append(line)
	return numbers

def add_left(node):
	value = node.left.value
	while True:
		parent = node.parent
		if not parent:
			return
		if parent.left is node:
			node = parent
		else:
			break
	node = parent.left
	while node.value is None:
		node = node.right
	node.value += value

def add_right(node):
	value = node.right.value
	while True:
		parent = node.parent
		if not parent:
			return
		if parent.right is node:
			node = parent
		else:
			break
	node = parent.right
	while node.value is None:
		node = node.left
	node.value += value

def explode(node, depth):
	if not node or node.value is not None:
		return False
	if depth == 4:
		add_left(node)
		add_right(node)
		node.left = None
		node.right = None
		node.value = 0
		return True
	return explode(node.left, depth+1) or explode(node.right, depth+1)

def split(node):
	if not node:
		return False
	if node.value is not None:
		if (value := node.value) >= 10:
			node.left = Node(node, value//2)
			node.right = Node(node, value - value//2)
			node.value = None
			return True
		return False
	return split(node.left) or split(node.right)

def reduce(node):
	while explode(node, 0) or split(node): pass

def add(n1, n2):
	n1.parent = n2.parent = node = Node(None)
	node.left = n1
	node.right = n2
	reduce(node)
	return node

def test_reduce():
	for example, expected in (
		('[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]'),
		('[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]'),
		('[[6,[5,[4,[3,2]]]],1]', '[[6,[5,[7,0]]],3]'),
		('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[7,0]]]]'),
		('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]', '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]'),
	):
		i, node = parse(example, 0, None)
		reduce(node)
		if str(node) != expected:
			print('Node', example, '=>', node, 'instead of', expected)

def part1(numbers):
	i, n1 = parse(numbers[0], 0, None)
	for j in range(1, len(numbers)):
		i, n2 = parse(numbers[j], 0, None)
		n1 = add(n1, n2)

	print('-------------------- Part 1 --------------------')
	print('The reduced sum is', n1)
	print('The magnitude is', abs(n1))

def part2(numbers):
	max_mag = 0
	max_mag_pairs = []
	for i, s1 in enumerate(numbers):
		for j, s2 in enumerate(numbers):
			if i == j: continue
			k, n1 = parse(s1, 0, None)
			k, n2 = parse(s2, 0, None)
			n1 = add(n1, n2)
			m = abs(n1)
			if m >= max_mag:
				if m > max_mag:
					max_mag = m
					max_mag_pairs.clear()
				max_mag_pairs.append((s1, s2, str(n1)))

	print('-------------------- Part 2 --------------------')
	print('The largest magnitude is', max_mag)
	for s1, s2, s3 in max_mag_pairs:
		print(s1, '+', s2)
		print('=', s3)

def main():
	numbers = read_input()
	if not numbers: return
	try:
		part1(numbers)
		part2(numbers)
	except ParseError as e:
		print(e)

if __name__ == '__main__':
	main()
