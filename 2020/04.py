import sys

def validate(passport):
	for field in ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'):
		if field not in passport:
			return False
	return True

def main():
	num_valid = 0
	passport = {}
	for line in sys.stdin:
		line = line.strip()
		if line:
			for field in line.split():
				k, v = field.split(':')
				passport[k] = v
		else:
			if validate(passport):
				num_valid += 1
			passport.clear()

	if validate(passport):
		num_valid += 1
	print(num_valid, 'valid passports')

if __name__ == '__main__':
	main()
