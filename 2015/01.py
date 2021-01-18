import sys

def main():
	data = sys.argv[1] if len(sys.argv) > 1 else sys.stdin.readline()

	floor = 0
	for c in data:
		if c == '(':
			floor += 1
		elif c == ')':
			floor -= 1
		elif c != '\n':
			sys.exit('Unexpected character!')
	print(floor)

if __name__ == '__main__':
	main()
