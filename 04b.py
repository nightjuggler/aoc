import sys
import re

year_pattern = re.compile('^[12][0-9]{3}$')
height_cm_pattern = re.compile('^1[0-9]{2}cm$')
height_in_pattern = re.compile('^[567][0-9]in$')
hair_color_pattern = re.compile('^#[0-9a-f]{6}$')
eye_color_pattern = re.compile('^[a-z]{3}$')
passport_id_pattern = re.compile('^[0-9]{9}$')

def check_byr(v):
	return year_pattern.match(v) and (1920 <= int(v) <= 2002)

def check_iyr(v):
	return year_pattern.match(v) and (2010 <= int(v) <= 2020)

def check_eyr(v):
	return year_pattern.match(v) and (2020 <= int(v) <= 2030)

def check_hgt(v):
	if height_cm_pattern.match(v):
		return 150 <= int(v[:3]) <= 193
	if height_in_pattern.match(v):
		return 59 <= int(v[:2]) <= 76
	return False

def check_hcl(v):
	return hair_color_pattern.match(v)

def check_ecl(v):
	return eye_color_pattern.match(v) and v in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')

def check_pid(v):
	return passport_id_pattern.match(v)

fields = (
	('byr', check_byr),
	('iyr', check_iyr),
	('eyr', check_eyr),
	('hgt', check_hgt),
	('hcl', check_hcl),
	('ecl', check_ecl),
	('pid', check_pid),
)

def validate(passport):
	for field, check in fields:
		value = passport.get(field)
		if not (value and check(value)):
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
