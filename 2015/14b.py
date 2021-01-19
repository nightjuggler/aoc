import argparse
import re
import sys

class Reindeer(object):
	def __init__(self, name, speed, fly_time, rest_time):
		self.name = name
		self.speed = int(speed)
		self.fly_time = int(fly_time)
		self.burst_time = self.fly_time + int(rest_time)
		self.points = 0
		self.distance = 0
		self.seconds = 0

	def tick(self):
		self.seconds += 1
		if self.seconds <= self.fly_time:
			self.distance += self.speed
		elif self.seconds == self.burst_time:
			self.seconds = 0

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('seconds', nargs='?', type=int, default=2503)
	args = parser.parse_args()

	line_pattern = re.compile('^([A-Z][a-z]+) can fly ([1-9][0-9]*) km/s for ([1-9][0-9]*) seconds, '
		'but then must rest for ([1-9][0-9]*) seconds\\.$')

	reindeer = []
	for line_number, line in enumerate(sys.stdin):
		m = line_pattern.match(line)
		if not m:
			print('Line {} doesn\'t match pattern!'.format(line_number))
			return
		reindeer.append(Reindeer(*m.groups()))

	leaders = set()
	max_distance = 0
	for burst in range(args.seconds):
		for r in reindeer:
			r.tick()
			if r.distance < max_distance:
				continue
			if r.distance > max_distance:
				max_distance = r.distance
				leaders.clear()
			leaders.add(r)
		for r in leaders:
			r.points += 1

	reindeer.sort(reverse=True, key=lambda r: r.points)
	for i, r in enumerate(reindeer, start=1):
		print('{}. {:8} {:6} km {:6} points'.format(i, r.name, r.distance, r.points))

if __name__ == '__main__':
	main()
