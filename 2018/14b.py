import sys

def main():
	target = '825401'
	if len(sys.argv) > 1:
		target = sys.argv[1]
		if not target.isdecimal():
			print('Please specify a string of digits!')
			return

	target = [int(d) for d in target]
	target_len = len(target)
	recipes = [3, 7]
	num_recipes = 2
	i1 = 0
	i2 = 1

	while recipes[num_recipes - target_len:] != target:
		elf1 = recipes[i1]
		elf2 = recipes[i2]
		new_recipe = elf1 + elf2
		if new_recipe >= 10:
			recipes.append(1)
			num_recipes += 1
			if recipes[num_recipes - target_len:] == target:
				break
			recipes.append(new_recipe - 10)
		else:
			recipes.append(new_recipe)
		num_recipes += 1
		i1 = (i1 + elf1 + 1) % num_recipes
		i2 = (i2 + elf2 + 1) % num_recipes

	print(num_recipes - target_len)

if __name__ == '__main__':
	main()
