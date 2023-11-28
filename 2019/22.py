import re
import sys

err = sys.exit

def read_input():
	p1 = re.compile('^cut (-?[1-9][0-9]*)$')
	p2 = re.compile('^deal with increment ([1-9][0-9]*)$')
	shuffles = []
	for i, line in enumerate(sys.stdin, start=1):
		if m := p1.match(line):
			shuffles.append((0, int(m.group(1))))
		elif m := p2.match(line):
			shuffles.append((1, int(m.group(1))))
		elif line.rstrip() == 'deal into new stack':
			shuffles.append((2, None))
		else:
			err(f'Input line {i} isn\'t a valid shuffle!')
	return shuffles

def shuffle_v1(actions, pos, size, reps):
	for _ in range(reps):
		for action, arg in actions:
			if action == 0:
				pos -= arg
			elif action == 1:
				pos *= arg
			else:
				pos = -(pos + 1)
			pos %= size
	return pos

def unshuffle_v1(actions, pos, size, reps):
	actions = actions[::-1]
	for _ in range(reps):
		for action, arg in actions:
			if action == 0:
				pos += arg
			elif action == 1:
				while pos % arg: pos += size
				pos //= arg
			else:
				pos = -(pos + 1)
			pos %= size
	return pos

def get_a_b(actions, size):
	#
	# Each of the three shuffle actions can be expressed as multiplying the
	# current position by some number "x" (possibly 1) and adding some number
	# "y" (possibly 0). These x's and y's can be grouped such that the final
	# position can be expressed in terms of the initial position multiplied
	# by a number "a" (the product of the x's) and adding a number "b". For
	# example, for initial position "pos" and three consecutive shuffle actions
	# (x1, y1), (x2, y2), and (x3, y3), the final position is given by
	#
	# ((pos*x1 + y1) * x2 + y2) * x3 + y3 = pos*x1*x2*x3 + (y1*x2*x3 + y2*x3 + y3)
	#
	# So a = x1*x2*x3 and b = y1*x2*x3 + y2*x3 + y3
	#
	a = 1
	b = 0
	for action, arg in actions:
		if action == 0:
			#
			# new_pos = old_pos - arg
			# So new_pos = old_pos*x + y where x=1 and y=-arg
			# Since old_pos = start_pos*a + b,
			# new_pos = (start_pos*a + b) - arg = start_pos*a + (b-arg)
			# So a is unchanged while b -= arg
			#
			b -= arg
		elif action == 1:
			#
			# new_pos = old_pos * arg
			# So new_pos = old_pos*x + y where x=arg and y=0
			# Since old_pos = start_pos*a + b,
			# new_pos = (start_pos*a + b) * arg = start_pos*a*arg + b*arg
			# So a *= arg and b *= arg
			#
			a *= arg
			b *= arg
		else:
			#
			# new_pos = -(old_pos + 1)
			# So new_pos = old_pos*x + y where x=-1 and y=-1
			# Since old_pos = start_pos*a + b,
			# new_pos = -((start_pos*a + b) + 1) = start_pos*(-a) - (b+1)
			# So a = -a and b = -(b+1)
			#
			a = -a
			b += 1
			b = -b
		a %= size
		b %= size
	return a, b

def shuffle(actions, pos, size, reps):
	a, b = get_a_b(actions, size)

	# Applying the shuffle actions once, new_pos = pos*a + b
	#
	# Each repetition of the shuffle process multiplies the previous
	# result by "a" and adds "b". So, for example, if reps == 3,
	#
	# new_pos = (((pos*a) + b)*a + b)*a + b
	#         = pos*a*a*a + (b*a*a + b*a + b)
	#         = pos*(a**3) + b*(a**2 + a**1 + a**0)
	#
	# new_pos = pos*(a**reps) + b*sum(a**i for i in range(reps))
	#
	# This is all mod "size". So we can compute a**reps using the mod
	# parameter of Python's built-in pow function:
	#
	a_pow_reps = pow(a, reps, size)

	# The sum of the geometric series sum(a**i for i in range(reps))
	# is (1 - a**reps) / (1 - a) = (a**reps - 1) / (a - 1)
	#
	# Since we're computing a**reps mod size, we must determine the
	# modular multiplicative inverse of (a - 1) mod size. Since size
	# is expected to be prime, we can simply use Euler's theorem:
	#
	# x**phi(p) = 1 (mod p)
	# => x**(phi(p)-1) = x**(-1) (mod p)
	# => x**((p-1)-1) = x**(-1) (mod p)
	# => x**(-1) = x**(p-2) (mod p)
	#
	# https://en.wikipedia.org/wiki/Modular_multiplicative_inverse#Using_Euler's_theorem
	#
	inv_a_minus_1 = pow(a-1, size-2, size)
	b_series = b * (a_pow_reps-1) * inv_a_minus_1 % size

	return (pos*a_pow_reps + b_series) % size

def unshuffle(actions, pos, size, reps):
	#
	# Here we're solving for start_pos in the following equation:
	#
	# start_pos*(a**reps) + b*sum(a**i for i in range(reps)) = pos (mod size)
	#
	a, b = get_a_b(actions, size)
	a_pow_reps = pow(a, reps, size)
	inv_a_pow_reps = pow(a_pow_reps, size-2, size)
	inv_a_minus_1 = pow(a-1, size-2, size)
	b_series = b * (a_pow_reps-1) * inv_a_minus_1 % size

	return (pos - b_series) % size * inv_a_pow_reps % size

def get_args():
	args = sys.argv[1:]
	if len(args) == 0:
		return None
	if len(args) != 4:
		err('Expected either no args or exactly four args!')

	func, pos, size, reps = args
	func_map = {
		'1': shuffle,
		'1v1': shuffle_v1,
		'2': unshuffle,
		'2v1': unshuffle_v1,
	}
	func = func_map.get(func)
	if not func:
		err(f'Please specify one of these functions: {", ".join(sorted(func_map))}')

	pos = int(pos)
	size = int(size)
	reps = int(reps)

	if pos < 0:
		err('The position cannot be negative!')
	if size < 1:
		err('The number of cards must be positive!')
	if pos >= size:
		err('The position must be less than the number of cards!')
	if reps < 1:
		err('The number of reps must be positive!')

	return func, pos, size, reps

def main():
	args = get_args()
	shuffles = read_input()
	if args:
		func, *args = args
		print(func(shuffles, *args))
	else:
		print('Part 1:', shuffle(shuffles, 2019, 10007, 1))
		print('Part 2:', unshuffle(shuffles, 2020, 119315717514047, 101741582076661))
main()
