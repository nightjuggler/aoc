import re
import sys

def err(message, *args):
	sys.exit(message.format(*args) if args else message)

def main():
	lines = sys.stdin.readlines()
	lines.sort()

	date_pattern = re.compile('^\\[1518-[0-9]{2}-[0-9]{2} ([0-9]{2}):([0-9]{2})\\] ')
	guard_pattern = re.compile('^Guard #([1-9][0-9]*) begins shift$')
	guards = {}
	asleep = None
	minutes = None

	for line in lines:
		m = date_pattern.match(line)
		if not m:
			err('Line doesn\'t match pattern!')

		hour, minute = map(int, m.groups())

		line = line[m.end():]
		if line == 'falls asleep\n':
			assert hour == 0
			assert minutes is not None
			assert asleep is None
			asleep = minute
			continue
		if line == 'wakes up\n':
			assert hour == 0
			assert minutes is not None
			assert asleep is not None
			for i in range(asleep, minute):
				minutes[i] += 1
			asleep = None
			continue

		m = guard_pattern.match(line)
		if not m:
			err('Line doesn\'t match pattern!')

		assert asleep is None
		guard = int(m.group(1))
		minutes = guards.get(guard)
		if minutes is None:
			guards[guard] = minutes = [0] * 60

	most_minutes = 0
	most_asleep_guards = []

	for guard, minutes in guards.items():
		sum_minutes = sum(minutes)
		if sum_minutes >= most_minutes:
			if sum_minutes > most_minutes:
				most_minutes = sum_minutes
				most_asleep_guards.clear()
			most_asleep_guards.append(guard)

	assert len(most_asleep_guards) == 1
	guard = most_asleep_guards[0]
	minutes = guards[guard]

	max_asleep = 0
	max_asleep_minutes = []

	for minute, asleep in enumerate(minutes):
		if asleep >= max_asleep:
			if asleep > max_asleep:
				max_asleep = asleep
				max_asleep_minutes.clear()
			max_asleep_minutes.append(minute)

	assert len(max_asleep_minutes) == 1
	minute = max_asleep_minutes[0]

	print(guard, '*', minute, '=', guard * minute)

if __name__ == '__main__':
	main()
