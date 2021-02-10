import sys

def main():
	lines = []
	for line in sys.stdin:
		line = line.rstrip()
		for prev in lines:
			diff = None
			assert len(prev) == len(line)
			for i, (a, b) in enumerate(zip(prev, line)):
				if a != b:
					if diff is None:
						diff = i
					else:
						diff = None
						break
			if diff is not None:
				a = line[:diff]
				b = line[diff + 1:]
				assert a == prev[:diff]
				assert b == prev[diff + 1:]
				print(a + b)
		lines.append(line)

if __name__ == '__main__':
	main()
