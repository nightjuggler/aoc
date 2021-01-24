import argparse
import re

def tokenize(s):
	max_i = len(s) - 1
	if max_i < 0:
		print('tokenize(): Expected non-empty string!')
		return []

	t = []
	i = 0
	a = ord(s[0])

	while True:
		if not (65 <= a <= 90):
			print('tokenize("{}"): Expected uppercase letter at position {}!'.format(s, i))
			break
		if i == max_i:
			t.append(chr(a))
			break
		i += 1
		b = ord(s[i])
		if 97 <= b <= 122:
			t.append(chr(a) + chr(b))
			if i == max_i:
				break
			i += 1
			a = ord(s[i])
		else:
			t.append(chr(a))
			a = b
	return t

def read_rules(f):
	line_pattern = re.compile('^(?:[A-Z][a-z]?|e) => (?:[A-Z][a-z]?)+$')

	rules = {}
	e_rules = set()
	rn_leaders = set()

	for i, line in enumerate(f, start=1):
		line = line.rstrip()
		if not line_pattern.match(line):
			if not line:
				break
			print('Line {} doesn\'t match pattern!'.format(i))
			continue
		a, b = line.split(' => ')
		b = tuple(tokenize(b))
		blen = len(b)
		assert a not in ('Ar', 'Rn', 'Y')
		assert b[0] not in ('Ar', 'Rn', 'Y')
		if blen == 1:
			assert a == 'e'
		elif blen == 2:
			assert b[1] not in ('Ar', 'Rn', 'Y')
		else:
			assert a != 'e'
			assert blen > 3
			assert b[1] == 'Rn'
			assert b[blen-1] == 'Ar'
			expect_y = False
			for i in range(2, blen-1):
				if expect_y:
					assert b[i] == 'Y'
				else:
					assert b[i] not in ('Ar', 'Rn', 'Y')
				expect_y = not expect_y
			rn_leaders.add(b[0])
		if a == 'e':
			assert b not in e_rules
			e_rules.add(b)
		else:
			assert b not in rules
			rules[b] = a

	return rules, e_rules, rn_leaders

def reduce_pairwise(rules, x):
	s = set()
	slen = 0

	def recurse(j):
		xlen = len(x)
		for i in range(j, xlen-1):
			prev = x[i:i+2]
			a = rules.get(tuple(prev))
			if a:
				x[i:i+2] = [a]
				recurse(0 if i < 2 else i-1)
				x[i:i+1] = prev
		nonlocal slen
		if slen == 0:
			slen = xlen
		elif xlen > slen:
			return
		elif xlen < slen:
			s.clear()
			slen = xlen
		s.add(tuple(x))

	recurse(0)
	assert len(s) == 1
	s = s.pop()
	if len(s) > 1:
		print('Cannot reduce to one element:', ''.join(x), '=>', ''.join(s))
	return s

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputfile', nargs='?', default='data/19.input')
	parser.add_argument('-v', '--verbose', action='store_true')
	args = parser.parse_args()

	verbose = args.verbose

	with open(args.inputfile) as f:
		rules, e_rules, rn_leaders = read_rules(f)
		m = tokenize(f.readline().rstrip())

	if verbose:
		print(''.join(m))

	i = 0
	rn_i = 0
	size = len(m)
	steps = 0

	def reduce_wrapper():
		nonlocal i, rn_i, size, steps
		p = m[rn_i:i]
		s = reduce_pairwise(rules, p)
		if e == 'Rn' and s[-1] not in rn_leaders:
			print('Not reducing', ''.join(p), '=>', ''.join(s), 'before Rn')
			return

		steps += len(p) - len(s)
		m[rn_i:i] = s
		size = len(m)
		i = rn_i + len(s)

		if verbose:
			print(''.join(p), '=>', ''.join(s))
			print(''.join(m))

	while i < size:
		e = m[i]
		if e in ('Ar', 'Rn', 'Y'):
			if i > rn_i + 1:
				reduce_wrapper()
			rn_i = i + 1
		i += 1
	if i > rn_i + 1:
		reduce_wrapper()

	i = 0
	rn = []
	while i < size:
		e = m[i]
		if e == 'Rn':
			rn.append([i])
		elif e == 'Ar':
			rn_i = rn.pop()[0]
			p = m[rn_i-1:i+1]
			a = rules.get(tuple(p))
			if verbose:
				print(''.join(p), '=>', a)
			assert a
			steps += 1
			m[rn_i-1:i+1] = [a]
			size = len(m)
			if verbose:
				print(''.join(m))
			i = rn_i
			rn_i = rn[-1][-1] + 1 if rn else 0
			while i < size:
				e = m[i]
				if e in ('Ar', 'Rn', 'Y'):
					if i > rn_i + 1:
						reduce_wrapper()
					break
				i += 1
			continue
		elif e == 'Y':
			rn[-1].append(i)
		i += 1

	if tuple(m) in e_rules:
		print('Reduced to e in', steps + 1, 'steps')
	else:
		print(''.join(m), 'cannot be reduced to e!')

if __name__ == '__main__':
	main()
