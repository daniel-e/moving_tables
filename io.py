def load_room(f):
	room = []
	for i in f:
		l = [c for c in i.rstrip()]
		room.append(l)
	return room

def load_table():
	table = []
	table_start_offset = []

	for i in open("tisch.txt"):
		l = [c for c in i.rstrip()]
		table.append(l)
	for (ypos, l) in enumerate(table):
		for (xpos, c) in enumerate(l):
			if c == 'O':
				table_start_offset.extend([xpos, ypos])

	return (table, table_start_offset)
