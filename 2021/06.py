import sys

def main(days):
	fishes = [0] * 9
	for n in sys.stdin.readline().split(','):
		fishes[int(n)] += 1

	for day in range(days):
		n = fishes.pop(0)
		fishes.append(n)
		fishes[6] += n

	print(sum(fishes))

if __name__ == '__main__':
	if len(sys.argv) == 1:
		main(80)
	elif len(sys.argv) != 2 or sys.argv[1] != '2':
		print('usage: wtf?')
	else:
		main(256)
