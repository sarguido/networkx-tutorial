# Get relationships between followers

import os
import oauth2 as oauth

from itertools import combinations, islice
from json import load, dump, dumps
from client import tapi, dapi
from time import sleep
import csv

f = open('../client/data/friends/list.PyTennessee.json')

data = load(f)

pytn_friends = [item['screen_name'] for item in data['users']]

combos = combinations(pytn_friends, 2)

item = islice(combos, 700)
item1 = islice(combos, 701, 1400)
item2 = islice(combos, 1401, 2100)
item3 = islice(combos, 2101, 2800)
item4 = islice(combos, 2801, 3500)
item5 = islice(combos, 3501, 4200)
item6 = islice(combos, 4201, 4900)
item7 = islice(combos, 4901, 5600)
item8 = islice(combos, 5601, 6300)
item9 = islice(combos, 6301, None)

itemlist = [item4, item5, item6, item7, item8, item9]

i = 4
for combo_item in itemlist:
	combos_data = {}

	for combo in combo_item:
		print 'Combo:', combo
		print 'Sleeping...'
		sleep(6.5)
		url = 'https://api.twitter.com/1.1/friendships/show.json?source_screen_name=%s&target_screen_name=%s' % (combo[0], combo[1])

		data = tapi.get_response(url)

		combo_str = str(combo[0]) + ' ' + str(combo[1])
		combos_data[combo_str] = data

	i += 1
	filename = 'pairs_%d.json' % i
	with open(filename, 'w') as fp:
		dump(combos_data, fp)
		print 'Next file'
