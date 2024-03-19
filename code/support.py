from csv import reader

def import_csv_layout(path):
	#import the map and create a 2D array with it
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map, delimiter=',')
		for row in layout:
			terrain_map.append(list(row))
		return terrain_map