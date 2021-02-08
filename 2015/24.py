import re
import sys

def err(message, *args):
	sys.exit(message.format(*args) if args else message)

def read_input(f):
	line_pattern = re.compile('^[1-9][0-9]*$')
	weights = []
	for i, line in enumerate(f, start=1):
		if not line_pattern.match(line):
			err('Line {} doesn\'t match pattern!', i)
		weights.append(int(line))
	return weights

def solve(weights, verbose=False):
	target, r = divmod(sum(weights), 3)
	if r != 0:
		err('The sum of the weights must be divisible by 3!')

	weights.sort()
	num_weights = len(weights)
	weights2 = weights.copy()
	min_qe = 0

	def check_qe():
		g1 = []
		g2 = []
		g3 = []
		for i in range(num_weights):
			w1 = weights[i]
			w2 = weights2[i]
			if w1 == 0:
				g1.append(w2)
			elif w2 == 0:
				g2.append(w1)
				weights2[i] = w1
			else:
				g3.append(w1)
		nonlocal min_qe
		qe = 1
		for w in g1:
			qe *= w
		if min_qe == 0 or qe < min_qe:
			min_qe = qe
		if verbose:
			print('QE =', qe)
			for g in (g1, g2, g3):
				print(' + '.join([str(w) for w in g]), '=', sum(g))

	def find_one(left, i=0):
		for j in range(i, num_weights):
			w = weights[j]
			if w == 0: continue
			left -= w
			if left < 0: break
			weights2[j] = 0
			if left == 0 or find_one(left, j + 1):
				return True
			weights2[j] = w
			left += w
		return False

	def find_all(left, size, i=0):
		for j in range(i, num_weights):
			w = weights[j]
			left -= w
			if left < 0: break
			weights[j] = 0
			if left == 0:
				if find_one(target): check_qe()
			elif size > 1:
				find_all(left, size - 1, j + 1)
			weights[j] = w
			left += w

	for size in range(1, num_weights // 3 + 1):
		min_qe = 0
		find_all(target, size)
		if min_qe:
			print('The minimum group size is', size)
			print('The minimum QE for any group of that size is', min_qe)
			break

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--verbose', '-v', action='store_true')
	args = parser.parse_args()

	solve(read_input(sys.stdin), args.verbose)

if __name__ == '__main__':
	main()
