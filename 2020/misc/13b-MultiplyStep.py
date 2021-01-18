import sys

def main(input):
	next(input)

	# Find t such that for each (i, bus), t % bus = (bus-i) % bus, i.e. t = bus-i (mod bus)

	buses = []
	for i, bus in enumerate(next(input).strip().split(',')):
		if bus != 'x':
			bus = int(bus)
			buses.append(((bus - i) % bus, bus))
	t = 0
	step = 1
	for remainder, bus in buses:
		while t % bus != remainder:
			t += step
		step *= bus
	print(t)

if __name__ == '__main__':
	main(sys.stdin)
