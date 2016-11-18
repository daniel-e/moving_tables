def load_room(f):
	room = []
	for i in f:
		l = [c for c in i.rstrip()]
		if len(l) > 0:
			room.append(l)
	return room

def load_escape(f):
	e = []
	cnt = []
	for i in f:
		l = [c for c in i.rstrip()]
		if len(l) > 0:
			e.append(l)
	for (ypos, l) in enumerate(e):
		for (xpos, c) in enumerate(l):
			if c == 'c':
				cnt = [xpos, ypos]
	return (e, cnt)

def get_table_start_offset(table):
	for (ypos, l) in enumerate(table):
		for (xpos, c) in enumerate(l):
			if c == 'c':
				return [xpos, ypos]

def load_table():
	table = []

	for i in open("tisch.txt"):
		l = [c for c in i.rstrip()]
		if len(l) > 0:
			table.append(l)

	table_start_offset = get_table_start_offset(table)

	return (table, table_start_offset)
