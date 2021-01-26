import re
import sys

def err(message, *args):
	sys.exit(message.format(*args) if args else message)

def read_boss(f):
	line_pattern = re.compile('^([A-Z][a-z]+(?: [A-Z][a-z]+)*): ([1-9][0-9]*|0)$')
	values = []
	for line_number, property_name in enumerate(('Hit Points', 'Damage', 'Armor'), start=1):
		line = f.readline()
		m = line_pattern.match(line)
		if not m:
			err('Boss line {} doesn\'t match pattern!', line_number)
		if m.group(1) != property_name:
			err('Boss line {}: Expected {}!', line_number, property_name)
		values.append(int(m.group(2)))
	return values

def read_shop(f):
	header_pattern = re.compile('^([A-Z][a-z]+): +Cost +Damage +Armor$')
	item_pattern = re.compile('^([A-Z][a-z]+(?: \\+[123])?) +([1-9][0-9]*) +([0-9]) +([0-9])$')
	shop = {'Weapons': [], 'Armor': [], 'Rings': []}
	line_number = 0

	for line in f:
		line_number += 1
		m = header_pattern.match(line)
		if not m:
			err('Shop line {} doesn\'t match header pattern!', line_number)
		category = m.group(1)
		items = shop.get(category)
		if items is None:
			err('Shop line {}: Unexpected category!', line_number)
		for line in f:
			line_number += 1
			m = item_pattern.match(line)
			if not m:
				if line.strip() == '': break
				err('Shop line {} doesn\'t match item pattern!', line_number)
			name, cost, damage, armor = m.groups()
			items.append((name, int(cost), int(damage), int(armor)))
	return shop

def get_armor(shop):
	armor = shop['Armor']
	yield ('No Armor', 0, 0, 0)
	for item in armor:
		yield item

def get_rings(shop):
	rings = shop['Rings']
	yield (('No Rings', 0, 0, 0),)
	for ring in rings:
		yield (ring,)
	for ring1 in rings:
		for ring2 in rings:
			if ring1 is not ring2:
				yield (ring1, ring2)

def get_items(shop):
	items = [None, None, None]
	for weapon in shop['Weapons']:
		items[0] = weapon
		for armor in get_armor(shop):
			items[1] = armor
			for rings in get_rings(shop):
				items[2:] = rings
				yield items

def main():
	with open('data/21.boss') as f:
		boss_hp, boss_damage, boss_armor = read_boss(f)
	with open('data/21.shop') as f:
		shop = read_shop(f)

	self_hp = 100
	min_cost = None
	min_cost_items = []

	for items in get_items(shop):
		total_cost = 0
		self_damage = 0
		self_armor = 0
		for item, cost, damage, armor in items:
			total_cost += cost
			self_damage += damage
			self_armor += armor
		self_attack = max(self_damage - boss_armor, 1)
		boss_attack = max(boss_damage - self_armor, 1)
		self_ttl, remainder = divmod(self_hp, boss_attack)
		if remainder:
			self_ttl += 1
		boss_ttl, remainder = divmod(boss_hp, self_attack)
		if remainder:
			boss_ttl += 1
		if self_ttl >= boss_ttl:
			if min_cost is None:
				min_cost = total_cost
			elif total_cost < min_cost:
				min_cost = total_cost
				min_cost_items.clear()
			elif total_cost > min_cost:
				continue
			min_cost_items.append(items.copy())

	for items in min_cost_items:
		print(min_cost, ', '.join([item[0] for item in items]))

if __name__ == '__main__':
	main()
