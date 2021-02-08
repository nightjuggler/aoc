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

def solve(weights, num_groups, verbose=False):
	if num_groups < 2:
		err('The number of groups must be greater than 1!')

	target, r = divmod(sum(weights), num_groups)
	if r != 0:
		err('The sum of the weights must be divisible by {}!', num_groups)

	weights.sort()
	num_weights = len(weights)
	weights2 = weights.copy()
	group2fill = 2 - num_groups
	min_qe = 0

	def check_qe():
		groups = [[] for i in range(num_groups)]
		n = num_groups - 1
		for i in range(num_weights):
			w = weights[i]
			w2 = weights2[i]
			if w == 0:
				groups[0].append(w2)
			elif w < 0:
				groups[n + w].append(w2)
				weights[i] = w2
			else:
				groups[n].append(w)
		nonlocal min_qe
		qe = 1
		for w in groups[0]:
			qe *= w
		if min_qe == 0 or qe < min_qe:
			min_qe = qe
		if verbose:
			print('QE =', qe)
			for g in groups:
				print(' + '.join([str(w) for w in g]), '=', sum(g))

	def find_one(left, x, i=0):
		for j in range(i, num_weights):
			w = weights[j]
			if w <= 0: continue
			left -= w
			if left < 0: break
			weights[j] = x
			if left == 0:
				if x + 1 == 0 or find_one(target, x + 1):
					return True
			elif find_one(left, x, j + 1):
				return True
			weights[j] = w
			left += w
		return False

	def find_all(left, size, i=0):
		for j in range(i, num_weights):
			w = weights[j]
			left -= w
			if left < 0: break
			weights[j] = 0
			if left == 0:
				if group2fill == 0 or find_one(target, group2fill):
					check_qe()
			elif size > 1:
				find_all(left, size - 1, j + 1)
			weights[j] = w
			left += w

	for size in range(1, num_weights // num_groups + 1):
		min_qe = 0
		find_all(target, size)
		if min_qe:
			print('The minimum group size is', size)
			print('The minimum QE for any group of that size is', min_qe)
			break

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--groups', '-g', type=int, default=4)
	parser.add_argument('--verbose', '-v', action='store_true')
	args = parser.parse_args()

	solve(read_input(sys.stdin), args.groups, args.verbose)

if __name__ == '__main__':
	main()
