from collections import defaultdict
from math import log10
import sys

def solve(stones, num_blinks):
	for _ in range(num_blinks):
		new_stones = defaultdict(int)
		for stone, count in stones.items():
			if not stone:
				new_stones[1] += count
				continue
			digits = int(log10(stone)) + 1
			if digits % 2:
				new_stones[stone * 2024] += count
				continue
			stone, stone2 = divmod(stone, 10**(digits//2))
			new_stones[stone] += count
			new_stones[stone2] += count
		stones = new_stones
	return sum(stones.values())

def main():
	stones = defaultdict(int)
	for stone in map(int, sys.stdin.read().split()):
		stones[stone] += 1
	print('Part 1:', solve(stones, 25))
	print('Part 2:', solve(stones, 75))

main()
