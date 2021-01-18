import sys

def main(input):
	min_wait = None
	min_wait_bus = None

	timestamp = int(next(input).strip())

	for bus in next(input).strip().split(','):
		if bus == 'x':
			continue
		bus = int(bus)
		m = timestamp % bus
		if m == 0:
			min_wait = 0
			min_wait_bus = bus
			break
		m = bus - m
		if min_wait is None or m < min_wait:
			min_wait = m
			min_wait_bus = bus

	print('Wait', min_wait, 'minutes for bus', min_wait_bus)
	print(min_wait_bus, '*', min_wait, '=', min_wait_bus * min_wait)

if __name__ == '__main__':
	main(sys.stdin)
