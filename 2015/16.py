import re

def read_mfcsam(filename):
	line_pattern = re.compile('^([a-z]+): (0|[1-9][0-9]*)$')
	compounds = {}
	with open(filename) as f:
		for line_number, line in enumerate(f, start=1):
			m = line_pattern.match(line)
			if not m:
				print('{}, line {} doesn\'t match pattern!'.format(filename, line_number))
			else:
				compounds[m.group(1)] = int(m.group(2))
	return compounds

def read_input(filename):
	prop_pattern = '[a-z]+: (?:0|[1-9][0-9]*)'
	line_pattern = re.compile('^Sue ([1-9][0-9]*): ({x}(?:, {x})*)$'.format(x=prop_pattern))

	sue_props = []
	with open(filename) as f:
		for line_number, line in enumerate(f, start=1):
			m = line_pattern.match(line)
			if not m:
				print('{}, line {} doesn\'t match pattern!'.format(filename, line_number))
				continue

			sue, line = m.groups()
			assert int(sue) == line_number

			props = []
			for prop in line.split(', '):
				k, v = prop.split(': ')
				props.append((k, int(v)))

			sue_props.append(props)
	return sue_props

def main():
	compounds = read_mfcsam('data/16.mfcsam')
	sue_props = read_input('data/16.input')

	for sue_number, props in enumerate(sue_props, start=1):
		for k, v in props:
			if compounds[k] != v:
				break
		else:
			print(sue_number)

if __name__ == '__main__':
	main()
