def load_room(f):
	room = []
	for i in f:
		l = [c for c in i.rstrip()]
		if len(l) > 0:
			room.append(l)
	return room

def load_escape():
	e = []
	cnt = []
	for i in open("escape.txt"):
		l = [c for c in i.rstrip()]
		if len(l) > 0:
			e.append(l)
	for (ypos, l) in enumerate(e):
		for (xpos, c) in enumerate(l):
			if c == 'c':
				cnt = [xpos, ypos]
	return (e, cnt)

def load_table():
	table = []
	table_start_offset = []

	for i in open("tisch.txt"):
		l = [c for c in i.rstrip()]
		if len(l) > 0:
			table.append(l)
	for (ypos, l) in enumerate(table):
		for (xpos, c) in enumerate(l):
			if c == 'c':
				table_start_offset.extend([xpos, ypos])

	return (table, table_start_offset)
