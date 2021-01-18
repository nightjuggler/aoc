import sys

def main():
	adapters = [int(line.strip()) for line in sys.stdin]
	adapters.sort()

	prev = 0
	prev_diff = 0
	prev2_diff = 0
	prev_paths = 1
	prev2_paths = 0
	prev3_paths = 0

	for n in adapters:
		diff = n - prev
		paths = prev_paths
		if diff == 1:
			if prev_diff == 2:
				paths += prev2_paths
			elif prev_diff == 1:
				paths += prev2_paths
				if prev2_diff == 1:
					paths += prev3_paths
		elif diff == 2:
			if prev_diff == 1:
				paths += prev2_paths
		elif diff != 3:
			sys.exit('Wtf?')
		prev = n
		prev2_diff = prev_diff
		prev_diff = diff
		prev3_paths = prev2_paths
		prev2_paths = prev_paths
		prev_paths = paths

	print(prev_paths, 'combinations')

if __name__ == '__main__':
	main()
