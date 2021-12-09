def main(reg0):
	reg5 = 4 * 19 * 11 + 4 * 22 + 15
	if reg0 == 1:
		reg5 += (27 * 28 + 29) * 30 * 14 * 32
		reg0 = 0
	for reg3 in range(1, reg5 + 1):
		if reg5 % reg3 == 0:
			reg0 += reg3
	print(reg0)

if __name__ == '__main__':
	main(1)
