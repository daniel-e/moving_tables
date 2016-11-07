import random

def cp_room(r):
	x = []
	for i in r:
		x.append(i[:])
	return x

def put_table(room, table, x, y, to_bin = False):
    for (ypos, l) in enumerate(table):
        for (xpos, c) in enumerate(l):
            if c != ' ':
                # check collisions with other tables
                if not to_bin:
                    if ypos + y >= len(room) or xpos + x >= len(room[ypos + y]) or room[ypos + y][xpos + x] != 'X':
                        return False
                if to_bin:
                    room[ypos + y][xpos + x] = "!"
                else:
                    room[ypos + y][xpos + x] = c
    return True

def put_tables(room, table, table_pos):
    r = cp_room(room)
    for x, y in table_pos:
        if not put_table(r, table, x, y):
            return None
    return r

def get_target_pos(room):
	for (ypos, y) in enumerate(room):
		for (xpos, x) in enumerate(y):
			if x == 'T':
				return [xpos, ypos]
	return None

def dist(x, y, tx, ty):
	return (tx - x) * (tx - x) + (ty - y) * (ty - y)

def find_valid_random_table_layout(n_tables, room, table):
	while True:
		pos = []
		r = cp_room(room)
		for i in xrange(n_tables):
			x = random.randint(0, len(room[0]) - 1)
			y = random.randint(0, len(room) - 1)
			if not put_table(r, table, x, y):
				break
			pos.append((x, y))
		if len(pos) == n_tables:
			return pos
