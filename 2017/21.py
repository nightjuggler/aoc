from collections import Counter, defaultdict
import re
import sys

def rotations(x):
	size = len(x)
	x = ''.join(x)
	x90 = ''.join([x[i::size] for i in range(size)][::-1])
	return x, x90, x[::-1], x90[::-1]

def read_input(f):
	p2 = '/'.join(['[#.]{2}'] * 2)
	p3 = '/'.join(['[#.]{3}'] * 3)
	p4 = '/'.join(['[#.]{4}'] * 4)
	r2 = re.compile(f'^({p2}) => ({p3})$')
	r3 = re.compile(f'^({p3}) => ({p4})$')
	lhs_map = {} # maps left-hand-side pattern string to rule number, e.g. '.#...####' => 0
	lhs_count = [] # maps rule number to the number of '#' in the left-hand-side pattern string
	rhs_list = [] # maps rule number to the right-hand-side pattern string
	for n, line in enumerate(f):
		if not (m := r2.match(line) or r3.match(line)):
			sys.exit(f'Line {n+1} doesn\'t match pattern!')
		lhs, rhs = m.groups()
		rhs_list.append(rhs.replace('/', ''))
		lhs_count.append(lhs.count('#'))
		lhs = lhs.split('/')
		lhs_map.update((x, n) for x in rotations(lhs))
		lhs_map.update((x, n) for x in rotations(lhs[::-1]))
	return lhs_map, lhs_count, rhs_list

def cut(x, old_size, new_size):
	m = new_size * old_size
	n = old_size * old_size
	assert len(x) == n
	return [''.join([x[k:k+new_size] for k in range(j, j+m, old_size)])
		for i in range(0, n, m)
		for j in range(i, i+old_size, new_size)]

def paste(xs, old_size, new_size):
	m = new_size // old_size
	n = old_size * old_size
	assert len(xs) == m*m
	return ''.join([xs[i+k][j:j+old_size]
		for i in range(0, m*m, m)
		for j in range(0, n, old_size)
		for k in range(m)])

def main():
	num_steps = int(sys.argv[1]) if len(sys.argv) > 1 else 5

	lhs_map, lhs_count, rhs_list = read_input(sys.stdin)

	step1_map = {}
	step2_map = {}
	step3_map = {}

	def get_rule(lhs):
		if lhs in lhs_map: return lhs_map[lhs]
		lhs_count.append(lhs.count('#'))
		size = 2 if len(lhs) == 4 else 3
		lhs = [lhs[i:i+size] for i in range(0, len(lhs), size)]
		rhs = ['.' * (size+1)] * (size+1)
		n = len(rhs_list)
		print(f'Adding rule {n}: {"/".join(lhs)} => {"/".join(rhs)}')
		rhs_list.append(''.join(rhs))
		lhs_map.update((x, n) for x in rotations(lhs))
		lhs_map.update((x, n) for x in rotations(lhs[::-1]))
		return n

	def make_step_maps(lhs):
		def check(xs): return list(map(get_rule, xs))

		# Step 1: Map lhs from 3x3 to 4x4 and cut into four 2x2's

		xs = check(cut(rhs_list[lhs], 4, 2))
		step1_map[lhs] = tuple(Counter(xs).items())

		# Step 2: Map each of the four 2x2's to 3x3. Then paste the four 3x3's
		# together into one 6x6. Then cut that into nine 2x2's

		xs = check(cut(paste([rhs_list[x] for x in xs], 3, 6), 6, 2))
		step2_map[lhs] = tuple(Counter(xs).items())

		# Step 3: Map each of the nine 2x2's to 3x3

		xs = check([rhs_list[x] for x in xs])
		step3_map[lhs] = tuple(Counter(xs).items())

		for lhs in xs:
			if lhs not in step3_map:
				make_step_maps(lhs)

	def do_steps(lhs, n):
		def update(c, step_map):
			new_c = defaultdict(int)
			for lhs, num_lhs in c.items():
				for x, num_x in step_map[lhs]:
					new_c[x] += num_lhs * num_x
			return new_c

		c = {lhs: 1}
		n, m = divmod(n, 3)
		for _ in range(n):
			c = update(c, step3_map)
		if m:
			c = update(c, step1_map if m == 1 else step2_map)

		return sum(lhs_count[x] * num_x for x, num_x in c.items())

	lhs = get_rule('.#./..#/###'.replace('/', ''))
	make_step_maps(lhs)
	print(do_steps(lhs, num_steps))

if __name__ == '__main__':
	main()
