import re
import sys

class Worker(object):
	def __init__(self):
		self.step = '.'
		self.time_left = 0

def main():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--workers', '-w', type=int, default=5)
	parser.add_argument('--basetime', '-t', type=int, default=60)
	args = parser.parse_args()

	num_workers = args.workers
	if num_workers < 1:
		print('The number of workers must be > 0!')
		return
	base_time = args.basetime
	if base_time < 0:
		print('The base time must be >= 0!')
		return

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

	workers = [Worker() for i in range(num_workers)]
	busy = 0
	time_spent = 0
	min_time_left = base_time + 26

	while True:
		i = 0
		while available and busy != num_workers:
			x = min(available)
			available.remove(x)
			while True:
				w = workers[i]
				i += 1
				if w.time_left == 0:
					break
			w.step = x
			w.time_left = base_time + ord(x) - ord('A') + 1
			if w.time_left < min_time_left:
				min_time_left = w.time_left
			busy += 1
		print('{:4}'.format(time_spent), '  '.join([w.step for w in workers]), ''.join(order), sep='  ')
		if not busy:
			break
		time_spent += min_time_left
		new_min_time_left = base_time + 26
		done = []
		for w in workers:
			if w.time_left == 0:
				continue
			w.time_left -= min_time_left
			if w.time_left == 0:
				x = w.step
				w.step = '.'
				done.append(x)
				busy -= 1
				for step in required_by[x]:
					steps = waiting_on[step]
					steps.remove(x)
					if not steps:
						available.add(step)
			elif w.time_left < new_min_time_left:
				new_min_time_left = w.time_left
		min_time_left = new_min_time_left
		order.extend(sorted(done))

if __name__ == '__main__':
	main()
