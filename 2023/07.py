from collections import Counter
import sys

def part1(hand):
	return sorted(Counter(hand).values(), reverse=True)

def part2(hand):
	c = Counter(hand)
	j = c.pop('J', 0)
	c = sorted(c.values(), reverse=True) if c else [0]
	c[0] += j
	return c

def rank(hands, cards, hand_type):
	cards = {c: i for i, c in enumerate(cards)}
	hands = [(hand_type(hand), [cards[c] for c in hand], int(bid)) for hand, bid in hands]
	hands.sort()
	return sum(i*hand[2] for i, hand in enumerate(hands, start=1))

def main():
	hands = [line.split() for line in sys.stdin]
	print('Part 1:', rank(hands, '23456789TJQKA', part1))
	print('Part 2:', rank(hands, 'J23456789TQKA', part2))
main()
