def main():
	h = 0
	for b in range(109900, 109900 + 17000 + 1, 17):
		for d in range(2, int(b**0.5) + 1):
			if not b % d:
				h += 1
				break
	print('Part 2:', h)
main()
