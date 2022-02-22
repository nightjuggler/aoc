import argparse

#   1       2      4     2
# 5   2 -> 1 4 -> 2 1 -> 4 -> 2
#  4 3      5

#   1        2       3
#  8 2     1   3    2 4      4       7      2     7
# 7   3 -> 8   4 -> 1 7 -> 3   7 -> 4 2 -> 7 4 -> 2 -> 7
#  6 4      7 6      8      2 1      3
#   5

def part2(n):
	next_elf = list(range(1, n+2))
	next_elf[n] = 1

	i = 1
	j = 1 + n//2
	prev_j = n//2

	for n in range(n, 1, -1):
		j = next_elf[prev_j] = next_elf[j]
		i = next_elf[i]
		if n % 2:
			prev_j = j
			j = next_elf[j]
	return i

# Recursive solution for part 1,
# derived from the following observation:
#
# After each elf has had one turn, the following elves remain:
# If n is even: all of the odd-numbered elves = range(1, n+1, 2)
# If n is odd: the odd-numbered elves starting with 3 (since the
# last odd-numbered elf (n) removes the first) = range(3, n+1, 2)
#
# So, in either case, the number of remaining elves is n//2, and
# the first remaining elf (let's call it first_elf) = 2*(n%2)+1.
# We can solve for n//2, subtract 1 from the result (since it will
# be between 1 and n//2), and use that as an index into the range
# of remaining elves. Thus:
#
# part1(n) = range(first_elf, n+1, 2)[part1(n//2)-1]
#          = 2*(n%2)+1 + 2*(part1(n//2)-1)
#
def part1(n):
	return 2*(n%2 + part1(n//2)) - 1 if n else 0

def next_pow2(n): return 1 << n.bit_length()
def next_pow2(n):
	x = 1
	while n:
		n >>= 1
		x <<= 1
	return x

# Non-recursive solution for part 1,
# derived from the recursive solution above.
#
def part1(n):
	return 2*n - next_pow2(n) + 1

def main():
	parser = argparse.ArgumentParser(allow_abbrev=False)
	parser.add_argument('elves', nargs='?', type=int, default=3014603)
	parser.add_argument('-2', '--part2', action='store_true')
	args = parser.parse_args()

	if args.elves <= 0:
		raise SystemExit('The number of elves must be greater than 0!')

	solve = part2 if args.part2 else part1

	print(solve(args.elves))

if __name__ == '__main__':
	main()
