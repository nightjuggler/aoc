import sys

def main():
	data = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.readline()

	floor = 0
	for i, c in enumerate(data, start=1):
		if c == '(':
			floor += 1
		elif c == ')':
			floor -= 1
		elif c != '\n':
			sys.exit('Unexpected character!')
		if floor == -1:
			print(i)
			break

if __name__ == '__main__':
	main()
