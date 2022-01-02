import sys

def supports_tls(line):
	abba = False
	hypernet = False
	for i in range(len(line) - 3):
		a = line[i]
		if a == '[':
			assert not hypernet
			hypernet = True
		elif a == ']':
			assert hypernet
			hypernet = False

		elif a == line[i+3] and a != (b := line[i+1]) and b == line[i+2] and b not in '[]':
			if hypernet:
				return False
			abba = True
	return abba

def supports_ssl(line):
	abas = set()
	babs = set()
	for i in range(len(line) - 2):
		a = line[i]
		if a in '[]':
			abas, babs = babs, abas

		elif a == line[i+2] and a != (b := line[i+1]) and b not in '[]':
			if (b, a) in babs:
				return True
			abas.add((a, b))
	return False

def main():
	lowercase = ''.join(map(chr, range(ord('a'), ord('z') + 1)))
	tls_count = 0
	ssl_count = 0

	for line in sys.stdin:
		line = line.rstrip()
		assert all([c in lowercase or c in '[]' for c in line])
		if supports_tls(line): tls_count += 1
		if supports_ssl(line): ssl_count += 1

	print('Part 1:', tls_count)
	print('Part 2:', ssl_count)

main()
