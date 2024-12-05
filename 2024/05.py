from collections import defaultdict
import sys

def main():
	sum1 = sum2 = 0
	rules = defaultdict(set)
	for line in sys.stdin:
		if line == '\n': break
		before, after = line.split('|')
		rules[int(after)].add(int(before))
	for line in sys.stdin:
		update = list(map(int, line.split(',')))
		after = set(update)
		n = len(update)
		i = j = 0
		while i < n:
			page = update[i]
			before = rules[page]
			if after.isdisjoint(before):
				after.remove(page)
				i += 1
				continue
			j = i + 1
			after_page = after.copy()
			while j < n:
				after_page.remove(update[j])
				if after_page.isdisjoint(before):
					break
				j += 1
			del update[i]
			update.insert(j, page)
		value = update[len(update)//2]
		if j:
			sum2 += value
		else:
			sum1 += value
	print('Part 1:', sum1)
	print('Part 2:', sum2)

main()
