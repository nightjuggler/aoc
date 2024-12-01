from collections import Counter
import sys

def get_lists():
	list1 = []
	list2 = []
	for line in sys.stdin:
		n1, n2 = line.split()
		list1.append(int(n1))
		list2.append(int(n2))
	return list1, list2

def part1(list1, list2):
	list1.sort()
	list2.sort()
	return sum(abs(n1-n2) for n1, n2 in zip(list1, list2))

def part2(list1, list2):
	list1 = Counter(list1)
	list2 = Counter(list2)
	return sum(n*c*list2[n] for n, c in list1.items())

def main():
	list1, list2 = get_lists()
	print('Part 1:', part1(list1, list2))
	print('Part 2:', part2(list1, list2))

if __name__ == '__main__':
	main()
