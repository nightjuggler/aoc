import argparse
import re
import sys

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('seconds', nargs='?', type=int, default=2503)
	args = parser.parse_args()

	seconds = args.seconds
	results = []

	line_pattern = re.compile('^([A-Z][a-z]+) can fly ([1-9][0-9]*) km/s for ([1-9][0-9]*) seconds, '
		'but then must rest for ([1-9][0-9]*) seconds\\.$')

	for line_number, line in enumerate(sys.stdin):
		m = line_pattern.match(line)
		if not m:
			print('Line {} doesn\'t match pattern!'.format(line_number))
			return
		name, speed, fly_time, rest_time = m.groups()
		speed = int(speed)
		fly_time = int(fly_time)
		rest_time = int(rest_time)
		cycles, time_remaining = divmod(seconds, fly_time + rest_time)
		distance = speed * (cycles * fly_time + min(fly_time, time_remaining))
		results.append((distance, name))

	results.sort(reverse=True)
	for i, (distance, name) in enumerate(results, start=1):
		print('{}. {:8} {:6} km'.format(i, name, distance))

if __name__ == '__main__':
	main()
