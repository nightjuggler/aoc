from collections import defaultdict, deque
import sys

def main():
	c = defaultdict(list)
	for i, line in enumerate(sys.stdin):
		a, b = map(int, line.split('/'))
		c[a].append((b, i))
		c[b].append((a, i))

	best1 = 0
	best2 = 0, 0
	q = deque()
	q.append((0, 0, frozenset()))
	while q:
		strength, a, used = q.pop()
		if strength > best1:
			best1 = strength
		length = len(used), strength
		if length > best2:
			best2 = length
		for b, i in c[a]:
			if i not in used:
				q.append((strength + a + b, b, used | {i}))

	print('Part 1:', best1)
	print('Part 2:', best2[1])
main()
