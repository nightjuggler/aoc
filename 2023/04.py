import sys

def read_input():
	def to_set(nums):
		return set(map(int, nums.split()))
	def matching(line):
		card, nums = line.split(':')
		want, have = nums.split('|')
		return len(to_set(want) & to_set(have))
	return list(map(matching, sys.stdin))

def part1(matching):
	return sum(2**(n-1) for n in matching if n)

def part2(matching):
	num_cards = len(matching)
	cards = [1] * num_cards
	for i, n in enumerate(matching):
		if n:
			m = cards[i]
			for j in range(i+1, min(i+n+1, num_cards)):
				cards[j] += m
	return sum(cards)

def main():
	matching = read_input()
	print('Part 1:', part1(matching))
	print('Part 2:', part2(matching))
main()
