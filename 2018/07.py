import re
import sys

def main():
	waiting_on = {} # maps x to the set of steps that must finish before x can begin
	required_by = {} # maps x to the set of steps that depend on x

	line_pattern = re.compile('^Step ([A-Z]) must be finished before step ([A-Z]) can begin.$')
	for i, line in enumerate(sys.stdin, start=1):
		m = line_pattern.match(line)
		if not m:
			print('Line {} doesn\'t match pattern!'.format(i))
			return
		a, b = m.groups()
		steps = waiting_on.get(b)
		if steps is None:
			waiting_on[b] = steps = set()
			required_by[b] = set()
		steps.add(a)
		steps = required_by.get(a)
		if steps is None:
			waiting_on[a] = set()
			required_by[a] = steps = set()
		steps.add(b)

	order = []
	available = set([step for step, steps in waiting_on.items() if not steps])
	while available:
		x = min(available)
		available.remove(x)
		order.append(x)
		for step in required_by[x]:
			steps = waiting_on[step]
			steps.remove(x)
			if not steps:
				available.add(step)
	print(''.join(order))

if __name__ == '__main__':
	main()
