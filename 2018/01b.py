import itertools
import sys

def main():
	freq = 0
	freqset = set()
	for x in itertools.cycle([int(x) for x in sys.stdin]):
		freq += x
		if freq in freqset:
			print(freq)
			break
		freqset.add(freq)

if __name__ == '__main__':
	main()
